---
last_updated: 2025-07-08T12:00:00Z
entry_count: 15
max_entries: 50
---

# Project Conventions & Patterns

## Naming Conventions
- Application name follows kebab-case format: "vibe-check-demo"

## Architecture Patterns
- Deployment scripts use environment-based configuration (staging/production)
- API modules use class-based architecture with dependency injection

## Common Dependencies
- Node.js/npm based build system (npm run build, npm test)
- Uses bcrypt for password hashing with 10 salt rounds
- Uses jsonwebtoken for JWT token generation
- PostgreSQL database with lib/pq driver in Go modules

## Security Patterns
- Password hashing with bcrypt is standard practice
- JWT tokens used for authentication (but secrets need proper configuration)
- Authentication methods throw generic Error objects without logging
- Database connections often disable SSL (security risk pattern)

## Performance Patterns
- Watch for N+1 query patterns in database operations
- Database modules lack connection pool configuration

## Testing Conventions
- No test files found for API modules (pattern to establish)

## Error Handling Patterns
- Database operations often lack comprehensive error handling
- Authentication errors use generic Error objects with simple messages
- Mixed error logging patterns (some logged, others not)
- Python logging utilities lack exception handling in constructors

## Frontend Component Patterns
- React components use TypeScript with proper interface definitions
- Components follow BEM CSS naming convention (button--variant)
- Functional components with hooks (useState, useCallback) preferred
- Components use external CSS imports with matching filename (Button.tsx → Button.css)