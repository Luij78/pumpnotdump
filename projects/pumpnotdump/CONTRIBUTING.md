# Contributing to pump.notdump.fun

Thank you for your interest in contributing to **pump.notdump.fun**! This project aims to protect Solana users from rug pulls through autonomous AI monitoring and on-chain enforcement.

## 🎯 Project Goals

- **Protect users** from rug pulls through autonomous monitoring
- **Enforce safety** via smart contract rules (not just alerts)
- **Maintain transparency** through open-source code and on-chain data
- **Build trust** in the Solana token launch ecosystem

## 🤝 How to Contribute

### 1. Reporting Bugs

If you find a bug, please open an issue with:
- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs. actual behavior**
- **Environment details** (Solana version, Node version, etc.)
- **Error messages or logs** if applicable

### 2. Suggesting Features

We welcome feature suggestions! Please open an issue with:
- **Use case:** Why is this feature needed?
- **Proposal:** How should it work?
- **Alternatives:** What other approaches did you consider?
- **Impact:** Who would benefit from this?

### 3. Submitting Pull Requests

**Before submitting a PR:**
1. Check existing issues/PRs to avoid duplicates
2. Discuss major changes in an issue first
3. Ensure your code follows our style guidelines
4. Add tests for new functionality
5. Update documentation as needed

**PR Process:**
```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes and commit
git commit -m "feat: add awesome feature"

# 4. Push to your fork
git push origin feature/your-feature-name

# 5. Open a Pull Request on GitHub
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding tests
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

## 🏗️ Development Setup

### Prerequisites
```bash
# Solana CLI (Agave 3.1.8)
sh -c "$(curl -sSfL https://release.anza.xyz/agave-v3.1.8/install)"

# Anchor CLI
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force
avm install 0.31.1
avm use 0.31.1

# Node.js 18+
brew install node  # or use nvm
```

### Local Development
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pumpnotdump.git
cd pumpnotdump

# Smart Contract Development
cd pumpnotdump
anchor build
anchor test

# Agent Development
cd agent
npm install
npm start
```

## 🧪 Testing Guidelines

**Smart Contract Tests:**
- All new instructions must have tests
- Test both success and failure cases
- Include boundary value tests (min/max amounts)
- Run full test suite: `anchor test`

**Agent Tests:**
- Test autonomous decision logic
- Mock blockchain responses when possible
- Test error handling and graceful degradation
- Verify forum post formatting

**Test Coverage Goals:**
- Smart contract: 80%+ instruction coverage
- Agent: 70%+ function coverage
- All critical paths tested

## 📝 Code Style

### Rust (Smart Contract)
- Follow Rust standard style (`rustfmt`)
- Use descriptive variable names
- Add comments for complex logic
- Keep functions focused and small
- Use `checked_add/sub` for all math

### TypeScript (Agent)
- Follow TypeScript best practices
- Use async/await (not callbacks)
- Type all function parameters
- Add JSDoc comments for public functions
- Handle errors gracefully

### Documentation
- Update README.md for user-facing changes
- Update ARCHITECTURE.md for technical changes
- Add inline comments for complex algorithms
- Keep examples up to date

## 🔒 Security Guidelines

**Critical Rules:**
1. **Never commit secrets** (API keys, private keys, passwords)
2. **Validate all inputs** (user data, blockchain data)
3. **Use checked math** (prevent overflows)
4. **Test edge cases** (zero amounts, max values)
5. **Follow principle of least privilege**

**Reporting Security Issues:**
- **DO NOT** open public issues for security vulnerabilities
- Email: luis.garcia@[domain] (replace with actual)
- Include: description, reproduction steps, potential impact
- We'll respond within 48 hours

## 🌟 Areas We Need Help

**High Priority:**
- Machine learning model for rug detection
- Frontend dashboard (Next.js + React)
- Additional smart contract tests
- Liquidity pool integration (Raydium/Orca)
- Multi-chain expansion (Ethereum, BSC)

**Good First Issues:**
- Documentation improvements
- Code comment additions
- Test coverage expansion
- Example scripts
- Bug fixes

## 📜 Code of Conduct

**Be Respectful:**
- Treat all contributors with respect
- Welcome diverse perspectives
- Assume good intentions
- Provide constructive feedback

**Be Professional:**
- Focus on the code, not the person
- Accept criticism gracefully
- Help newcomers learn
- Give credit where due

**Be Collaborative:**
- Discuss before making major changes
- Review PRs promptly
- Share knowledge freely
- Build together

## 🎖️ Recognition

Contributors will be recognized in:
- README.md contributors section
- GitHub releases
- Project documentation
- Social media shoutouts (with permission)

## 📞 Getting Help

- **Questions:** Open a GitHub Discussion
- **Real-time chat:** Join our Discord (coming soon)
- **Email:** [Contact info]
- **X/Twitter:** [@luij78](https://twitter.com/luij78)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make Solana safer! 🛡️**

Every contribution, no matter how small, helps protect users from rug pulls.
