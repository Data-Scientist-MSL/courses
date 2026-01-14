# CoursePlayerApp Certificate Display Specification

## Overview

The Certificate Display component showcases student achievements by presenting earned certificates with tier-based features including LinkedIn sharing, digital wallet integration, and blockchain verification for Advanced tier users.

---

## Certificate Showcase Features

### Certificate Gallery View

**Layout**: Grid of earned certificates with preview images

**Display Elements**:
- **Certificate Thumbnail**: Preview image (300x200px)
- **Course Title**: Name of completed course
- **Issue Date**: When certificate was earned
- **Grade/Score**: Final course grade (if applicable)
- **Verification Badge**: Visual indicator of verification status

**UI Implementation**:
```python
# courseplayerapp/ui/pages/certificates.py

import streamlit as st
from courseplayerapp.integrations.certificationexam_client import CertificationExamClient

def render_certificates_page(user_tier: str):
    """Render certificates showcase page."""
    
    st.title("🎓 Your Certificates")
    st.caption("Showcase your achievements and share with the world")
    
    # Fetch user certificates
    cert_client = CertificationExamClient()
    certificates = cert_client.get_user_certificates(st.session_state.user_id)
    
    if not certificates:
        st.info("You haven't earned any certificates yet. Complete a course to earn your first certificate!")
        return
    
    # Display statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Certificates", len(certificates))
    with col2:
        avg_grade = sum(c.grade for c in certificates if c.grade) / len(certificates)
        st.metric("Average Grade", f"{avg_grade:.1f}%")
    with col3:
        recent = max(c.issue_date for c in certificates)
        st.metric("Most Recent", recent.strftime("%b %Y"))
    
    # Certificate grid
    st.subheader("Certificate Gallery")
    
    # 3 columns for grid layout
    cols = st.columns(3)
    
    for idx, cert in enumerate(certificates):
        with cols[idx % 3]:
            render_certificate_card(cert, user_tier)
```

---

## Tier-Based Certificate Features

### All Tiers (Basic, Intermediate, Advanced)

**Standard Features**:
- ✅ Course completion certificate
- ✅ Download as PDF
- ✅ QR code verification link
- ✅ Public verification page
- ✅ View in gallery

### Intermediate & Advanced Tiers

**Additional Features**:
- ✅ Share to LinkedIn (one-click)
- ✅ Add to digital wallet (Apple Wallet, Google Pay)
- ✅ Professional certificate template
- ✅ Share via email/social media

### Advanced Tier Only

**Premium Features**:
- ✅ Blockchain-verified certificates
- ✅ Premium certificate template
- ✅ Custom branding (company logo)
- ✅ NFT certificate option (experimental)

---

## Certificate Templates

### Template Designs

```python
CERTIFICATE_TEMPLATES = {
    "basic": {
        "name": "Standard Template",
        "background": "classic_border.png",
        "font": "Georgia",
        "color_scheme": "blue_gold",
        "features": ["course_title", "user_name", "date", "qr_code"]
    },
    "intermediate": {
        "name": "Professional Template",
        "background": "modern_gradient.png",
        "font": "Helvetica Neue",
        "color_scheme": "teal_silver",
        "features": ["course_title", "user_name", "date", "grade", "linkedin_badge", "qr_code"]
    },
    "advanced": {
        "name": "Premium Template",
        "background": "luxury_marble.png",
        "font": "Futura",
        "color_scheme": "purple_gold",
        "features": ["course_title", "user_name", "date", "grade", "honors", "blockchain_badge", "qr_code", "custom_logo"]
    }
}
```

### Certificate Generation

```python
# courseplayerapp/integrations/certificationexam_client.py

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import qrcode
import io

class CertificateGenerator:
    """Generate PDF certificates with tier-specific templates."""
    
    def __init__(self, user_tier: str):
        self.tier = user_tier
        self.template = CERTIFICATE_TEMPLATES[user_tier]
    
    def generate_certificate_image(
        self,
        course_title: str,
        user_name: str,
        issue_date: datetime,
        grade: float = None,
        certificate_id: str = None,
        blockchain_hash: str = None
    ) -> Image:
        """
        Generate certificate image based on tier template.
        
        Args:
            course_title: Name of the course
            user_name: Student's name
            issue_date: Date certificate was issued
            grade: Final grade (optional)
            certificate_id: Unique certificate ID for verification
            blockchain_hash: Blockchain transaction hash (Advanced tier only)
        
        Returns:
            PIL Image object
        """
        # Load background template
        background_path = f"assets/templates/{self.template['background']}"
        img = Image.open(background_path)
        draw = ImageDraw.Draw(img)
        
        # Load fonts
        title_font = ImageFont.truetype(f"assets/fonts/{self.template['font']}.ttf", 48)
        name_font = ImageFont.truetype(f"assets/fonts/{self.template['font']}.ttf", 60)
        body_font = ImageFont.truetype(f"assets/fonts/{self.template['font']}.ttf", 24)
        
        # Draw certificate text
        # Title
        draw.text((400, 100), "EdGuide Certificate of Completion", 
                  font=title_font, fill='#1a1a1a', anchor='mm')
        
        # User name
        draw.text((400, 200), user_name, 
                  font=name_font, fill='#000080', anchor='mm')
        
        # Course title
        course_text = f"has successfully completed\n{course_title}"
        draw.text((400, 300), course_text, 
                  font=body_font, fill='#1a1a1a', anchor='mm', align='center')
        
        # Grade (if applicable and tier allows)
        if grade and self.tier in ['intermediate', 'advanced']:
            grade_text = f"Final Grade: {grade:.1f}%"
            if grade >= 95:
                grade_text += " - With Honors"
            draw.text((400, 400), grade_text, 
                     font=body_font, fill='#006400', anchor='mm')
        
        # Issue date
        date_text = f"Issued on {issue_date.strftime('%B %d, %Y')}"
        draw.text((400, 480), date_text, 
                  font=body_font, fill='#1a1a1a', anchor='mm')
        
        # QR code for verification
        if certificate_id:
            qr = qrcode.QRCode(version=1, box_size=3, border=1)
            verification_url = f"https://gai-observe.online/verify/{certificate_id}"
            qr.add_data(verification_url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Paste QR code on certificate
            img.paste(qr_img.resize((100, 100)), (50, 450))
            draw.text((100, 560), f"Verify: gai-observe.online/verify", 
                     font=ImageFont.truetype(f"assets/fonts/{self.template['font']}.ttf", 10), 
                     fill='#666666')
        
        # Blockchain badge (Advanced tier only)
        if blockchain_hash and self.tier == 'advanced':
            badge = Image.open("assets/icons/blockchain_verified.png").resize((40, 40))
            img.paste(badge, (720, 450), badge)
            draw.text((720, 500), "Blockchain Verified", 
                     font=ImageFont.truetype(f"assets/fonts/{self.template['font']}.ttf", 10), 
                     fill='#4a90e2', anchor='mm')
        
        return img
    
    def generate_pdf(
        self,
        course_title: str,
        user_name: str,
        issue_date: datetime,
        **kwargs
    ) -> bytes:
        """Generate PDF version of certificate."""
        img = self.generate_certificate_image(course_title, user_name, issue_date, **kwargs)
        
        # Convert to PDF
        pdf_buffer = io.BytesIO()
        img_rgb = img.convert('RGB')
        img_rgb.save(pdf_buffer, format='PDF', quality=95)
        pdf_buffer.seek(0)
        
        return pdf_buffer.getvalue()
```

---

## Integration with CertificationExam

### Fetching Certificates

```python
# courseplayerapp/integrations/certificationexam_client.py

import httpx
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class Certificate(BaseModel):
    """Certificate data model."""
    id: str
    user_id: str
    course_id: str
    course_title: str
    issue_date: datetime
    grade: Optional[float] = None
    certificate_url: str  # URL to certificate PDF
    verification_url: str  # Public verification page
    blockchain_hash: Optional[str] = None  # For Advanced tier
    blockchain_verified: bool = False

class CertificationExamClient:
    """Client for interacting with CertificationExam service."""
    
    def __init__(self, base_url: str = "https://certification.gai-observe.online"):
        self.base_url = base_url
    
    async def get_user_certificates(self, user_id: str) -> List[Certificate]:
        """
        Fetch all certificates earned by a user.
        
        Args:
            user_id: User identifier
        
        Returns:
            List of Certificate objects
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/certificates/user/{user_id}",
                headers={"Authorization": f"Bearer {get_api_token()}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return [Certificate(**cert) for cert in data["certificates"]]
            else:
                return []
    
    async def get_certificate_by_id(self, certificate_id: str) -> Optional[Certificate]:
        """
        Fetch a specific certificate by ID.
        
        Args:
            certificate_id: Unique certificate identifier
        
        Returns:
            Certificate object or None if not found
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/certificates/{certificate_id}",
                headers={"Authorization": f"Bearer {get_api_token()}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return Certificate(**data)
            else:
                return None
    
    async def verify_certificate(self, certificate_id: str) -> dict:
        """
        Verify certificate authenticity (public endpoint, no auth required).
        
        Args:
            certificate_id: Certificate ID to verify
        
        Returns:
            {
                "valid": True/False,
                "certificate": Certificate object if valid,
                "blockchain_verified": True/False
            }
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/certificates/verify/{certificate_id}"
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"valid": False, "certificate": None}
```

---

## Certificate Display UI

### Certificate Card Component

```python
# courseplayerapp/ui/components/certificate_card.py

import streamlit as st
from datetime import datetime

def render_certificate_card(certificate, user_tier: str):
    """Render individual certificate card with tier-specific features."""
    
    with st.container():
        # Certificate image/thumbnail
        st.image(
            certificate.thumbnail_url or generate_certificate_thumbnail(certificate),
            use_column_width=True
        )
        
        # Course title
        st.subheader(certificate.course_title)
        
        # Issue date and grade
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"📅 {certificate.issue_date.strftime('%b %d, %Y')}")
        with col2:
            if certificate.grade:
                st.caption(f"📊 Grade: {certificate.grade:.1f}%")
        
        # Download PDF (all tiers)
        if st.button(f"📄 Download PDF", key=f"download_{certificate.id}"):
            pdf_data = download_certificate_pdf(certificate.id)
            st.download_button(
                "Save Certificate",
                data=pdf_data,
                file_name=f"certificate_{certificate.course_id}.pdf",
                mime="application/pdf",
                key=f"save_{certificate.id}"
            )
        
        # LinkedIn share (Intermediate+)
        if user_tier in ["intermediate", "advanced"]:
            linkedin_url = generate_linkedin_share_url(
                certificate_name=certificate.course_title,
                issue_date=certificate.issue_date,
                certificate_url=certificate.verification_url
            )
            st.link_button(
                "🔗 Share on LinkedIn",
                linkedin_url,
                use_container_width=True
            )
            
            # Digital wallet
            if st.button(f"📱 Add to Wallet", key=f"wallet_{certificate.id}"):
                wallet_pass = generate_wallet_pass(certificate)
                st.download_button(
                    "Download Pass",
                    data=wallet_pass,
                    file_name=f"certificate_{certificate.id}.pkpass",
                    mime="application/vnd.apple.pkpass",
                    key=f"wallet_download_{certificate.id}"
                )
        else:
            st.info("💎 Upgrade to Intermediate to share on LinkedIn")
        
        # Verification
        st.caption(f"🔍 [Verify Certificate]({certificate.verification_url})")
        
        # Blockchain badge (Advanced only)
        if user_tier == "advanced" and certificate.blockchain_verified:
            st.success("✅ Blockchain Verified")
            with st.expander("View Blockchain Details"):
                st.code(certificate.blockchain_hash, language="text")
                st.link_button(
                    "View on Blockchain Explorer",
                    f"https://etherscan.io/tx/{certificate.blockchain_hash}"
                )
        elif user_tier != "advanced":
            st.caption("💎 Upgrade to Advanced for blockchain-verified certificates")
        
        st.divider()
```

---

## LinkedIn Integration

### One-Click LinkedIn Sharing

```python
# courseplayerapp/integrations/linkedin_share.py

from urllib.parse import urlencode

def generate_linkedin_share_url(
    certificate_name: str,
    issue_date: datetime,
    certificate_url: str,
    organization_name: str = "EdGuide",
    organization_id: str = None  # LinkedIn org ID
) -> str:
    """
    Generate LinkedIn certification share URL.
    
    Opens LinkedIn's "Add Certification" form pre-filled with certificate details.
    
    Args:
        certificate_name: Name of the certification/course
        issue_date: Date certificate was issued
        certificate_url: Public verification URL
        organization_name: Issuing organization (EdGuide)
        organization_id: LinkedIn organization ID (optional)
    
    Returns:
        LinkedIn share URL
    """
    # LinkedIn Add Certification URL format
    base_url = "https://www.linkedin.com/profile/add"
    
    params = {
        "startTask": "CERTIFICATION_NAME",
        "name": certificate_name,
        "organizationName": organization_name,
        "issueYear": issue_date.year,
        "issueMonth": issue_date.month,
        "certUrl": certificate_url,
        "certId": certificate_url.split('/')[-1]  # Extract cert ID from URL
    }
    
    if organization_id:
        params["organizationId"] = organization_id
    
    return f"{base_url}?{urlencode(params)}"


# Example usage
"""
User clicks "Share on LinkedIn" button:
-> Opens: https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME&name=Machine+Learning+Fundamentals&organizationName=EdGuide&issueYear=2026&issueMonth=1&certUrl=https://gai-observe.online/verify/abc123

LinkedIn shows pre-filled form:
- Certification Name: Machine Learning Fundamentals
- Issuing Organization: EdGuide
- Issue Date: January 2026
- Credential URL: https://gai-observe.online/verify/abc123

User clicks "Save" and certification appears on their LinkedIn profile.
"""
```

---

## Digital Wallet Integration

### Apple Wallet Pass

```python
# courseplayerapp/integrations/wallet_pass.py

from passbook import Pass, Barcode, StoreCard
import json

def generate_apple_wallet_pass(certificate: Certificate) -> bytes:
    """
    Generate Apple Wallet pass (.pkpass file) for certificate.
    
    Args:
        certificate: Certificate object
    
    Returns:
        Binary .pkpass file data
    """
    # Create pass
    pass_obj = Pass()
    pass_obj.passTypeIdentifier = "pass.online.gai-observe.certificate"
    pass_obj.organizationName = "EdGuide"
    pass_obj.teamIdentifier = "EDGUIDE_TEAM_ID"
    pass_obj.serialNumber = certificate.id
    pass_obj.description = f"Certificate: {certificate.course_title}"
    
    # Add barcode for verification
    pass_obj.barcode = Barcode(
        message=certificate.verification_url,
        format="QR"
    )
    
    # Create store card (generic pass type for certificates)
    store_card = StoreCard()
    
    # Header field
    store_card.addHeaderField(
        key="issuer",
        label="Issued By",
        value="EdGuide"
    )
    
    # Primary field
    store_card.addPrimaryField(
        key="course",
        label="Course Completed",
        value=certificate.course_title
    )
    
    # Secondary fields
    store_card.addSecondaryField(
        key="date",
        label="Issue Date",
        value=certificate.issue_date.strftime("%B %d, %Y")
    )
    
    if certificate.grade:
        store_card.addSecondaryField(
            key="grade",
            label="Grade",
            value=f"{certificate.grade:.1f}%"
        )
    
    # Auxiliary fields
    store_card.addAuxiliaryField(
        key="cert_id",
        label="Certificate ID",
        value=certificate.id
    )
    
    # Back fields (additional info)
    store_card.addBackField(
        key="verification",
        label="Verify Certificate",
        value=certificate.verification_url
    )
    
    pass_obj.storeCard = store_card
    
    # Generate .pkpass file
    pass_file = pass_obj.create(
        certificate_path="path/to/certificate.pem",
        key_path="path/to/private_key.pem",
        wwdr_certificate_path="path/to/wwdr.pem",
        password="pass_password"
    )
    
    return pass_file

def generate_google_wallet_pass(certificate: Certificate) -> str:
    """
    Generate Google Wallet pass (returns JWT token for Add to Google Wallet button).
    
    Args:
        certificate: Certificate object
    
    Returns:
        JWT token for Google Wallet
    """
    # Google Wallet requires JWT token
    # Implementation would use Google Wallet API
    # Return a "Add to Google Wallet" button URL
    
    pass_object = {
        "iss": "edguide@google-wallet.iam.gserviceaccount.com",
        "aud": "google",
        "typ": "savetowallet",
        "payload": {
            "genericObjects": [{
                "id": f"edguide_cert_{certificate.id}",
                "classId": "edguide_certificate_class",
                "logo": {
                    "sourceUri": {
                        "uri": "https://gai-observe.online/logo.png"
                    }
                },
                "cardTitle": {
                    "defaultValue": {
                        "language": "en-US",
                        "value": "EdGuide Certificate"
                    }
                },
                "header": {
                    "defaultValue": {
                        "language": "en-US",
                        "value": certificate.course_title
                    }
                },
                "barcode": {
                    "type": "QR_CODE",
                    "value": certificate.verification_url
                }
            }]
        }
    }
    
    # Sign JWT and return
    # (requires Google Wallet API setup)
    return "signed_jwt_token"
```

---

## Blockchain Verification (Advanced Tier)

### Certificate on Blockchain

```python
# courseplayerapp/integrations/blockchain_cert.py

from web3 import Web3
import json

class BlockchainCertification:
    """Issue and verify certificates on blockchain (Advanced tier only)."""
    
    def __init__(self):
        # Connect to Ethereum network (or other blockchain)
        self.w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/YOUR_PROJECT_ID"))
        self.contract_address = "0x_EDGUIDE_CERTIFICATE_CONTRACT"
        
        # Load contract ABI
        with open("contracts/CertificateRegistry.json") as f:
            contract_abi = json.load(f)
        
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=contract_abi
        )
    
    def issue_certificate_on_chain(
        self,
        certificate_id: str,
        user_wallet_address: str,
        course_hash: str,
        metadata_uri: str
    ) -> str:
        """
        Issue certificate as blockchain record.
        
        Args:
            certificate_id: Unique certificate ID
            user_wallet_address: User's Ethereum wallet address
            course_hash: Hash of course content (proves course version)
            metadata_uri: IPFS URI with certificate metadata
        
        Returns:
            Transaction hash
        """
        # Build transaction
        tx = self.contract.functions.issueCertificate(
            certificateId=certificate_id,
            recipient=user_wallet_address,
            courseHash=course_hash,
            metadataURI=metadata_uri
        ).buildTransaction({
            'from': EDGUIDE_WALLET_ADDRESS,
            'nonce': self.w3.eth.get_transaction_count(EDGUIDE_WALLET_ADDRESS),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign and send transaction
        signed_tx = self.w3.eth.account.sign_transaction(tx, EDGUIDE_PRIVATE_KEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for confirmation
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return receipt['transactionHash'].hex()
    
    def verify_certificate_on_chain(self, certificate_id: str) -> dict:
        """
        Verify certificate exists on blockchain.
        
        Args:
            certificate_id: Certificate ID to verify
        
        Returns:
            {
                "valid": True/False,
                "recipient": wallet_address,
                "issue_timestamp": unix_timestamp,
                "metadata_uri": ipfs_uri
            }
        """
        try:
            cert_data = self.contract.functions.getCertificate(certificate_id).call()
            
            return {
                "valid": cert_data[0],  # exists
                "recipient": cert_data[1],
                "issue_timestamp": cert_data[2],
                "metadata_uri": cert_data[3]
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}
```

### Smart Contract (Solidity)

```solidity
// CertificateRegistry.sol
pragma solidity ^0.8.0;

contract CertificateRegistry {
    struct Certificate {
        bool exists;
        address recipient;
        uint256 issueTimestamp;
        bytes32 courseHash;
        string metadataURI;
    }
    
    mapping(string => Certificate) public certificates;
    address public owner;
    
    event CertificateIssued(
        string indexed certificateId,
        address indexed recipient,
        uint256 issueTimestamp
    );
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can issue certificates");
        _;
    }
    
    function issueCertificate(
        string memory certificateId,
        address recipient,
        bytes32 courseHash,
        string memory metadataURI
    ) public onlyOwner {
        require(!certificates[certificateId].exists, "Certificate already exists");
        
        certificates[certificateId] = Certificate({
            exists: true,
            recipient: recipient,
            issueTimestamp: block.timestamp,
            courseHash: courseHash,
            metadataURI: metadataURI
        });
        
        emit CertificateIssued(certificateId, recipient, block.timestamp);
    }
    
    function getCertificate(string memory certificateId) 
        public 
        view 
        returns (bool, address, uint256, string memory) 
    {
        Certificate memory cert = certificates[certificateId];
        return (cert.exists, cert.recipient, cert.issueTimestamp, cert.metadataURI);
    }
    
    function verifyCertificate(string memory certificateId) 
        public 
        view 
        returns (bool) 
    {
        return certificates[certificateId].exists;
    }
}
```

---

## Public Verification Page

### Certificate Verification Endpoint

```python
# courseplayerapp/api/verify.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/verify/{certificate_id}")
async def verify_certificate_page(certificate_id: str):
    """
    Public certificate verification page (no authentication required).
    
    Args:
        certificate_id: Certificate ID to verify
    
    Returns:
        HTML page with certificate details
    """
    # Fetch certificate from CertificationExam
    cert_client = CertificationExamClient()
    verification = await cert_client.verify_certificate(certificate_id)
    
    if not verification["valid"]:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    cert = verification["certificate"]
    
    # Generate HTML page
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Verify Certificate - EdGuide</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
            .certificate-card {{ border: 2px solid #4a90e2; border-radius: 10px; padding: 30px; background: #f9f9f9; }}
            .valid-badge {{ color: green; font-size: 24px; }}
            .info-row {{ margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="certificate-card">
            <h1>✅ Certificate Verified</h1>
            <p class="valid-badge">This certificate is authentic and issued by EdGuide.</p>
            
            <div class="info-row"><strong>Course:</strong> {cert.course_title}</div>
            <div class="info-row"><strong>Issue Date:</strong> {cert.issue_date.strftime("%B %d, %Y")}</div>
            <div class="info-row"><strong>Certificate ID:</strong> {cert.id}</div>
            
            {f'<div class="info-row"><strong>Grade:</strong> {cert.grade:.1f}%</div>' if cert.grade else ''}
            
            {f'<div class="info-row"><strong>Blockchain:</strong> <a href="https://etherscan.io/tx/{cert.blockchain_hash}">View on Etherscan</a></div>' if cert.blockchain_verified else ''}
            
            <p style="margin-top: 30px; color: #666;">
                <small>This certificate can be verified at: https://gai-observe.online/verify/{cert.id}</small>
            </p>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-14  
**Author**: EdGuide Certification Team  
**Platform**: EdGuide (gai-observe.online)
