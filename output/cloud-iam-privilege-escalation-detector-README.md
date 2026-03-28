# Cloud IAM Privilege Escalation Detector

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.5+-blue.svg)](https://typescriptlang.org)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org)
[![AWS](https://img.shields.io/badge/AWS-Cloud-orange.svg)](https://aws.amazon.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.8+-FF6F00.svg)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent cloud security system that leverages graph neural networks and machine learning to continuously monitor AWS IAM policies and CloudTrail logs, detecting privilege escalation paths and excessive permissions in real-time.

## 🎯 Overview

This system addresses critical cloud security challenges by:
- **Analyzing IAM relationships** using graph neural networks to model complex permission structures
- **Detecting anomalous access patterns** through advanced ML algorithms on CloudTrail data
- **Identifying privilege escalation paths** before they can be exploited
- **Providing automated risk scoring** and policy recommendations
- **Enabling proactive governance** through continuous monitoring and alerting

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CloudTrail    │────│   Lambda         │────│   S3 Bucket     │
│   Log Stream    │    │   Data Ingestion │    │   Raw Logs      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   IAM Policy    │────│   Graph Builder  │────│   NetworkX      │
│   Scanner       │    │   (GNN Model)    │    │   Graph DB      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React         │────│   Risk Engine    │────│   TensorFlow    │
│   Dashboard     │    │   API Gateway    │    │   ML Models     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Datadog        │
                       │   Monitoring     │
                       └──────────────────┘
```

## 🚀 Setup Instructions

### Prerequisites
- AWS Account with IAM, CloudTrail, Lambda, and S3 access
- Python 3.8+
- Node.js 16+
- Terraform (optional, for infrastructure)

### Backend Setup
```bash
# Clone repository
git clone https://github.com/victoriab37/iam-privilege-escalation-detector.git
cd iam-privilege-escalation-detector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure

# Set environment variables
export AWS_REGION=us-east-1
export S3_BUCKET=your-cloudtrail-bucket
export DATADOG_API_KEY=your-datadog-key
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### AWS Infrastructure
```bash
# Deploy Lambda functions and IAM roles
cd infrastructure
terraform init
terraform apply
```

## 💻 Usage

### Running the Detection System
```python
from detector import IAMPrivilegeDetector

# Initialize detector
detector = IAMPrivilegeDetector(
    cloudtrail_bucket="your-bucket",
    monitoring_interval=300  # 5 minutes
)

# Start continuous monitoring
detector.start_monitoring()

# Get risk assessment for specific user
risk_score = detector.assess_user_risk("user-arn")
print(f"Risk Score: {risk_score}")

# Generate policy recommendations
recommendations = detector.get_policy_recommendations("role-arn")
```

### Graph Analysis
```python
from graph_analyzer import IAMGraphAnalyzer

# Build IAM relationship graph
analyzer = IAMGraphAnalyzer()
graph = analyzer.build_iam_graph()

# Detect privilege escalation paths
escalation_paths = analyzer.find_escalation_paths(
    start_principal="arn:aws:iam::account:user/username",
    target_permissions=["admin", "s3:*"]
)

# Visualize relationships
analyzer.visualize_graph(output_path="iam_relationships.png")
```

### Dashboard Access
Navigate to `http://localhost:3000` to access the React dashboard featuring:
- Real-time risk scoring visualization
- Interactive IAM relationship graphs  
- Policy recommendation engine
- Anomaly detection alerts
- Compliance reporting

## 🧠 Key Concepts Learned

### Graph Neural Networks for Security
- **Node Embeddings**: Representing IAM entities (users, roles, policies) as vectors in high-dimensional space
- **Edge Classification**: Using GNNs to identify risky permission relationships
- **Graph Convolution**: Propagating security context through IAM hierarchies
- **Temporal Graph Analysis**: Tracking permission changes over time

### Advanced Anomaly Detection
- **Behavioral Baseline Modeling**: Establishing normal access patterns using statistical methods
- **Ensemble Methods**: Combining multiple ML models for robust anomaly detection  
- **Time Series Analysis**: Detecting unusual spikes in privilege usage
- **Contextual Anomalies**: Identifying suspicious actions based on user context

### Cloud Security