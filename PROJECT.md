# 🚀 AuricDefence

_A decentralized cybersecurity incident reporting system leveraging blockchain to ensure privacy, transparency, and secure threat intelligence sharing._

---

## 📖 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Challenges Faced](#challenges-faced)
- [Innovative Features](#innovative-features)
- [Setup & Installation](#setup--installation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## About the Project

Cybersecurity incident reporting is often centralized, risking censorship, tampering, and privacy breaches. Organizations are hesitant to share threat intelligence due to confidentiality concerns. **AuricDefence** solves this problem by:

✅ Providing decentralized, immutable evidence storage on blockchain.  
✅ Allowing anonymous reporting via Decentralized Identities (DID) and zk-SNARKs.  
✅ Enabling privacy-compliant threat intelligence sharing.  
✅ Offering user control over personal data in compliance with GDPR.

---

## Features

- **Decentralized Incident Reporting**  
  Anonymous reporting with DID and zk-SNARKs ensures privacy and security.

- **Immutable Storage**  
  Blockchain ledger records incident metadata and evidence hashes permanently.

- **Incident Tracking**  
  Smart contracts and event listeners track investigation progress.

- **Threat Intelligence Sharing**  
  Asymmetric cryptography enables secure sharing of intelligence between verified nodes.

- **User Data Management**  
  Portal for users to view, download, or delete their personal data.

- **Expert Assistance**  
  Secure chat/helpdesk connects users with cybersecurity professionals 24/7.

---

## Architecture

**Backend:**
- Python Flask for API development and WebSockets.
- Web3.py for blockchain integration.
- Cryptography libraries for encryption.
- IPFS API for decentralized storage.

**Frontend:**
- HTML, CSS, JavaScript for responsive UI.
- ethers.js and web3.js for blockchain interactions.

**Blockchain:**
- Ethereum (Solidity smart contracts) or Hyperledger Fabric.
- zk-SNARKs for privacy-preserving proofs.
- IPFS for decentralized file storage.

**Cybersecurity:**
- Security monitoring with PyOD for anomaly detection.
- Log analysis via Elasticsearch.
- Celery tasks for incident response workflows.
- Compliance checks for GDPR and other regulations.

**Database:**
- PostgreSQL for structured off-chain data.

**Authentication:**
- OAuth 2.0 for non-anonymous users.
- Decentralized Identity (DID) for anonymous users.
- JWT for session management.

**Deployment:**
- Docker containers.
- Kubernetes orchestration.
- CI/CD pipelines for automated deployments.

---

## Tech Stack

| Technology         | Purpose                                      |
|---------------------|----------------------------------------------|
| **Python Flask**    | Backend APIs, WebSockets                    |
| **Ethereum / Hyperledger** | Blockchain ledger and smart contracts |
| **Solidity**        | Smart contract development                  |
| **IPFS**            | Decentralized storage for large files       |
| **Web3.py**         | Blockchain integration from Python          |
| **ethers.js, web3.js** | Blockchain integration from frontend     |
| **zk-SNARKs Libraries** | Privacy-preserving proofs               |
| **PyOD**            | Anomaly detection in logs                   |
| **Elasticsearch**   | Log storage and searching                   |
| **PostgreSQL**      | Off-chain structured data                   |
| **Docker, Kubernetes** | Containerization and orchestration      |

---

## Challenges Faced

- Balancing privacy with traceability of incident reports.
- Handling blockchain transaction latency and gas fees.
- Managing large file storage via off-chain solutions like IPFS.
- Integrating decentralized identities and zk-SNARKs for anonymity.

---

## Innovative Features

- **zk-SNARKs** for anonymous incident reporting.
- Blockchain-based tracking of investigation progress.
- GDPR-compliant user data management portal.
- Asymmetric cryptography for secure, private threat sharing.

---

## Setup & Installation

> **Prerequisites:**
> - Python 3.9+
> - Node.js & npm
> - Docker
> - Ganache or testnet for blockchain testing

1. **Clone the repository**
    ```bash
    git clone https://github.com/your-username/auricdefence.git
    cd auricdefence
    ```
2.🐍 Backend Setup (Python + Flask)
Create and activate a virtual environment
```
python -m venv backend
source backend/bin/activate       # For Linux/macOS
backend\Scripts\activate          # For Windows

```
3.Install required Python libraries
```
pip install flask flask_sqlalchemy flask_bcrypt email-validator web3 cryptography ipfshttpclient pyjwt
```
4.Run the Flask server
```
python app.py
```
Ensure app.py contains your Flask app and is correctly configured with routes and blockchain logic.


---

## Testing

- Unit tests using **pytest**.
- Integration tests for blockchain and backend interactions.
- UI testing via **Selenium**.
- Manual security testing for smart contracts and APIs.

---

## Deployment

- Dockerized services for easy deployment.
- Kubernetes for horizontal scalability.
- GitHub Actions used for CI/CD pipelines.
- Smart contracts deployed to testnets like Rinkeby or Hyperledger Fabric dev networks.

---

## Future Improvements

- Optimize zk-SNARK circuits for speed.
- Implement Layer 2 scaling for reduced gas fees.
- Enhance frontend UX with dashboards for incident visualization.
- Add mobile app support for incident reporting.
- Integrate AI-driven threat intelligence analysis.

---

## License

This project is licensed under the MIT License.

---

**AuricDefence** — Securing cybersecurity collaboration through decentralization and privacy.
