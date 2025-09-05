# MindCare - Digital Mental Health Support System

A comprehensive digital platform providing psychological support, AI-powered assistance, and professional counseling services for students in higher education.

## 🌟 Features

### Student Portal
- **Mental Health Assessments**: Standardized PHQ-9 and GAD-7 assessments
- **AI Chatbot**: 24/7 AI-powered mental health assistant with crisis detection
- **Mood Tracking**: Visual charts and progress monitoring
- **Resource Library**: Self-help guides, CBT techniques, and educational content
- **Appointment Booking**: Schedule sessions with licensed counselors
- **Crisis Support**: Immediate access to emergency resources and hotlines

### Counselor Dashboard
- **Student Roster**: Manage students with consent-based access
- **Risk Assessment**: Monitor student mental health trends
- **Appointment Management**: Schedule and manage counseling sessions
- **Resource Management**: Create and share therapeutic materials
- **Crisis Alerts**: Immediate notifications for high-risk situations

### Admin Panel
- **System Analytics**: Aggregated usage metrics and trends
- **User Management**: Manage students, counselors, and system access
- **Resource Oversight**: Monitor and update mental health resources
- **Compliance Monitoring**: Ensure data privacy and security standards

### AI & Safety Features
- **RAG-Powered Chatbot**: Retrieval-Augmented Generation for contextual responses
- **Crisis Detection**: Automatic identification of self-harm indicators
- **Safety Guardrails**: Prevents medical advice and inappropriate responses
- **Multi-language Support**: English and Hindi language options
- **WCAG 2.1 AA Compliance**: Full accessibility support

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   React/Next.js │◄──►│   Node.js/      │◄──►│   PostgreSQL    │
│   TypeScript    │    │   Express       │    │   + Redis       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│   AI Pipeline   │──────────────┘
                        │   Python/RAG    │
                        │   Vector DB     │
                        └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### 1. Clone Repository
```bash
git clone https://github.com/your-org/mindcare.git
cd mindcare
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Docker Deployment (Recommended)
```bash
# Start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Manual Setup (Development)

#### Frontend
```bash
# Install dependencies
pnpm install

# Start development server
pnpm run dev
```

#### Backend
```bash
cd backend
npm install

# Run database migrations
npm run migrate

# Seed sample data
npm run seed

# Start development server
npm run dev
```

#### AI Pipeline
```bash
cd ai-pipeline
pip install -r requirements.txt

# Create sample training data
python train_embeddings.py --create-sample

# Train embeddings
python train_embeddings.py --data-path ./data --output-path ./models
```

## 📊 Database Schema

### Core Tables
- **users**: Student, counselor, and admin accounts
- **assessments**: PHQ-9 and GAD-7 assessment results
- **appointments**: Counseling session scheduling
- **resources**: Mental health educational content
- **chat_sessions**: AI chatbot interactions (encrypted)
- **system_logs**: Audit trail and security monitoring

### Security Features
- Row Level Security (RLS) policies
- Encrypted sensitive data fields
- JWT-based authentication
- Role-based access control (RBAC)
- Rate limiting and input validation

## 🤖 AI Integration

### RAG System
The AI chatbot uses Retrieval-Augmented Generation:

1. **Document Processing**: Mental health resources are embedded using Sentence Transformers
2. **Vector Storage**: FAISS index for fast similarity search
3. **Context Retrieval**: Relevant resources retrieved for each query
4. **Response Generation**: LLM generates contextual, safe responses

### Safety Guardrails
- Crisis keyword detection
- Medical advice prevention
- Inappropriate content filtering
- Automatic escalation protocols

## 🔒 Security & Privacy

### Data Protection
- End-to-end encryption for sensitive data
- HIPAA-compliant data handling
- Consent-based data sharing
- Regular security audits

### Access Control
- Multi-factor authentication
- Role-based permissions
- Session management
- API rate limiting

## 🧪 Testing

### Frontend Tests
```bash
pnpm run test
pnpm run test:e2e
```

### Backend Tests
```bash
cd backend
npm run test
npm run test:integration
```

### AI Pipeline Tests
```bash
cd ai-pipeline
python -m pytest tests/
```

## 📈 Monitoring & Analytics

### Health Checks
- `/health` endpoint for service monitoring
- Database connection status
- Redis connectivity
- AI model availability

### Metrics
- User engagement analytics
- Assessment completion rates
- Crisis intervention statistics
- System performance metrics

## 🚀 Deployment

### Production Deployment
```bash
# Build and deploy with Docker
docker-compose -f docker-compose.prod.yml up -d

# Or deploy to cloud platforms
# Vercel (Frontend)
vercel deploy

# Railway (Backend)
railway deploy

# DigitalOcean (Full Stack)
doctl apps create --spec .do/app.yaml
```

### Environment Variables
See `.env.example` for all required configuration options.

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Assessment Endpoints
- `POST /api/assessments` - Submit assessment
- `GET /api/assessments` - Get user assessments
- `GET /api/assessments/stats` - Assessment statistics

### Chat Endpoints
- `POST /api/chat/message` - Send message to AI
- `GET /api/chat/history/:sessionId` - Get chat history
- `POST /api/chat/escalate` - Report crisis situation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines
- Follow TypeScript/JavaScript best practices
- Write comprehensive tests
- Update documentation
- Ensure accessibility compliance
- Follow security guidelines

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Crisis Resources
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911

### Technical Support
- Create an issue on GitHub
- Email: support@mindcare.dev
- Documentation: [docs.mindcare.dev](https://docs.mindcare.dev)

## 🙏 Acknowledgments

- Mental health professionals who provided guidance
- Open source community for tools and libraries
- Students who participated in user testing
- University partners for collaboration

---

**⚠️ Important Disclaimer**: This platform provides educational resources and support tools but is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified mental health professionals with any questions you may have regarding a mental health condition.