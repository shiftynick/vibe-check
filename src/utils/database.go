package utils

import (
    "database/sql"
    "fmt"
    "log"
    "time"
    
    _ "github.com/lib/pq"
)

type Database struct {
    conn *sql.DB
    config DBConfig
}

type DBConfig struct {
    Host     string
    Port     int
    User     string
    Password string
    DBName   string
}

// NewDatabase creates a new database connection
func NewDatabase(config DBConfig) (*Database, error) {
    psqlInfo := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
        config.Host, config.Port, config.User, config.Password, config.DBName)
    
    db, err := sql.Open("postgres", psqlInfo)
    if err != nil {
        return nil, err
    }
    
    // Test connection
    err = db.Ping()
    if err != nil {
        return nil, err
    }
    
    return &Database{
        conn: db,
        config: config,
    }, nil
}

// ExecuteQuery runs a SQL query - SQL injection vulnerability!
func (d *Database) ExecuteQuery(query string) (*sql.Rows, error) {
    // Direct query execution without parameterization
    return d.conn.Query(query)
}

// GetUser fetches a user by ID
func (d *Database) GetUser(userID string) (map[string]interface{}, error) {
    // SQL injection vulnerability
    query := fmt.Sprintf("SELECT * FROM users WHERE id = %s", userID)
    
    rows, err := d.conn.Query(query)
    if err != nil {
        log.Printf("Query error: %v", err)
        return nil, err
    }
    defer rows.Close()
    
    // Memory leak - not closing rows in error cases
    columns, _ := rows.Columns()
    values := make([]interface{}, len(columns))
    valuePtrs := make([]interface{}, len(columns))
    
    for rows.Next() {
        for i := range columns {
            valuePtrs[i] = &values[i]
        }
        
        rows.Scan(valuePtrs...)
        
        result := make(map[string]interface{})
        for i, col := range columns {
            result[col] = values[i]
        }
        
        return result, nil
    }
    
    return nil, fmt.Errorf("user not found")
}

// Close closes the database connection
func (d *Database) Close() error {
    return d.conn.Close()
}