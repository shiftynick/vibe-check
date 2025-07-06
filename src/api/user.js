// User API module
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

class UserAPI {
  constructor(db) {
    this.db = db;
  }

  async createUser(email, password, role) {
    // TODO: Add input validation
    const hashedPassword = await bcrypt.hash(password, 10);
    
    const user = {
      email: email,
      password: hashedPassword,
      role: role || 'user',
      createdAt: new Date()
    };
    
    return this.db.users.insert(user);
  }

  async authenticate(email, password) {
    const user = await this.db.users.findOne({ email });
    
    if (!user) {
      throw new Error('User not found');
    }
    
    // Potential timing attack vulnerability
    const valid = await bcrypt.compare(password, user.password);
    
    if (!valid) {
      throw new Error('Invalid password');
    }
    
    // Hardcoded secret - security issue
    const token = jwt.sign({ id: user.id, email: user.email }, 'supersecret123');
    
    return { user, token };
  }

  async getAllUsers() {
    // N+1 query problem
    const users = await this.db.users.find({});
    
    for (let user of users) {
      user.posts = await this.db.posts.find({ userId: user.id });
    }
    
    return users;
  }
}

module.exports = UserAPI;