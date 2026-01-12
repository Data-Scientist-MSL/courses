# Certificate Display Specification

## Platform Information
- **Platform**: EdGuide
- **Domain**: gai-observe.online
- **Purpose**: Define certificate showcase and integration with CertificationExam

---

## Overview

The Certificate Display system showcases earned certificates, provides multiple sharing options, and integrates with the CertificationExam system. Certificates are tier-differentiated to reflect the value of each license level.

---

## Certificate Tiers

### Certificate Variations by Tier

| Feature | Basic ($97) | Intermediate ($247) | Advanced ($497) |
|---------|-------------|---------------------|-----------------|
| **Template** | Standard | Professional | Premium |
| **Design Quality** | Basic template | Enhanced design | Designer-crafted |
| **Verification** | QR code + URL | QR code + URL | QR code + URL + Blockchain |
| **Download Formats** | PDF | PDF + PNG | PDF + PNG + SVG |
| **LinkedIn Integration** | ❌ No | ✅ One-click share | ✅ One-click share + auto-fill |
| **Digital Wallet** | ❌ No | ❌ No | ✅ Apple Wallet + Google Pay |
| **Blockchain Verified** | ❌ No | ❌ No | ✅ Immutable record |
| **Customization** | None | Limited | Full (name display options) |
| **Portfolio Page** | Basic | Enhanced | Premium with analytics |

---

## Certificate Templates

### Basic Tier - Standard Certificate

**Design Elements**:
```yaml
basic_certificate:
  template: "standard_v1"
  
  content:
    - EdGuide Logo (top center)
    - Certificate of Completion heading
    - Student name (centered, serif font)
    - Course title
    - Completion date
    - Certificate ID (unique)
    - Instructor signature (digital)
    - QR code (verification)
    
  colors:
    primary: "#2C3E50"  # Dark blue
    accent: "#3498DB"   # Light blue
    text: "#333333"
    
  fonts:
    heading: "Georgia, serif"
    body: "Arial, sans-serif"
    
  dimensions:
    width: "8.5 inches"
    height: "11 inches"
    orientation: "portrait"
```

**Preview**:
```
┌─────────────────────────────────────────┐
│                                         │
│         [EdGuide Logo]                  │
│                                         │
│      CERTIFICATE OF COMPLETION          │
│                                         │
│         Presented to                    │
│                                         │
│         John Doe                        │
│                                         │
│    For successfully completing          │
│                                         │
│  Machine Learning Fundamentals          │
│                                         │
│      Date: January 12, 2026             │
│      Certificate ID: ML-2026-001234     │
│                                         │
│  [Instructor Signature]    [QR Code]    │
│                                         │
│  Verify: gai-observe.online/verify/...  │
│                                         │
└─────────────────────────────────────────┘
```

### Intermediate Tier - Professional Certificate

**Enhanced Features**:
- Professional color scheme
- Enhanced typography
- Course completion statistics
- LinkedIn-ready format
- Skill badges

```yaml
intermediate_certificate:
  template: "professional_v1"
  
  additional_content:
    - Course hours completed
    - Final grade/score
    - Key skills learned (badges)
    - LinkedIn logo integration
    - Professional border design
    
  premium_elements:
    - Subtle background pattern
    - Gold accent color
    - Enhanced signature area
    - Skills section
```

### Advanced Tier - Premium Certificate

**Exclusive Features**:
- Designer-crafted layout
- Custom branding options
- Blockchain verification badge
- Enhanced verification URL
- Multiple format exports

```yaml
advanced_certificate:
  template: "premium_v1"
  
  exclusive_content:
    - Blockchain verification badge
    - Detailed course statistics
    - Instructor bio/photo
    - Course outline summary
    - Digital wallet compatibility
    - Verifiable credentials (W3C standard)
    
  premium_design:
    - Metallic accents (gold/silver)
    - Premium paper texture background
    - Embossed seal effect
    - Multiple language support
```

---

## Certificate Generation

### Integration with CertificationExam

```python
# integrations/certificationexam_client.py

class CertificationExamClient:
    async def get_user_certificates(
        self,
        user_id: str
    ) -> List[Certificate]:
        """
        Retrieve all certificates for a user
        
        Returns:
            List of Certificate objects
        """
        
        response = await http_client.get(
            f"{CERTIFICATIONEXAM_API}/certificates",
            params={"user_id": user_id}
        )
        
        return [
            Certificate(
                certificate_id=cert["id"],
                course_id=cert["course_id"],
                course_title=cert["course_title"],
                issue_date=cert["issue_date"],
                grade=cert["grade"],
                tier=cert["tier"],
                pdf_url=cert["pdf_url"],
                png_url=cert.get("png_url"),
                verification_url=cert["verification_url"],
                blockchain_tx_id=cert.get("blockchain_tx_id"),
                skills=cert.get("skills", [])
            )
            for cert in response["certificates"]
        ]
    
    async def download_certificate(
        self,
        certificate_id: str,
        format: str = "pdf"
    ) -> bytes:
        """
        Download certificate in specified format
        
        Args:
            certificate_id: Unique certificate ID
            format: pdf, png, or svg (Advanced tier only)
        
        Returns:
            Certificate file bytes
        """
        
        response = await http_client.get(
            f"{CERTIFICATIONEXAM_API}/certificates/{certificate_id}/download",
            params={"format": format}
        )
        
        return response.content
    
    async def verify_certificate(
        self,
        certificate_id: str
    ) -> dict:
        """
        Verify certificate authenticity
        
        Returns:
            {
                "valid": True,
                "student_name": "John Doe",
                "course": "Machine Learning Fundamentals",
                "issue_date": "2026-01-12",
                "blockchain_verified": True,
                "blockchain_tx": "0x..."
            }
        """
        
        response = await http_client.get(
            f"{CERTIFICATIONEXAM_API}/verify/{certificate_id}"
        )
        
        return response
```

---

## Certificate Display UI

### Certificate Gallery View

```python
# ui/pages/certificates.py

import streamlit as st

def render_certificates_page(user_id, user_tier):
    """Render certificates gallery"""
    
    st.title("🎓 Your Certificates")
    
    # Get user certificates
    cert_client = CertificationExamClient()
    certificates = await cert_client.get_user_certificates(user_id)
    
    if not certificates:
        st.info("📚 No certificates yet. Complete a course to earn your first certificate!")
        return
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Certificates Earned", len(certificates))
    
    with col2:
        avg_grade = sum(cert.grade for cert in certificates) / len(certificates)
        st.metric("Average Grade", f"{avg_grade:.1f}%")
    
    with col3:
        skills = set()
        for cert in certificates:
            skills.update(cert.skills)
        st.metric("Skills Acquired", len(skills))
    
    st.markdown("---")
    
    # Display filter
    view_mode = st.radio(
        "View",
        ["Gallery", "List", "Timeline"],
        horizontal=True
    )
    
    if view_mode == "Gallery":
        render_certificate_gallery(certificates, user_tier)
    elif view_mode == "List":
        render_certificate_list(certificates, user_tier)
    else:
        render_certificate_timeline(certificates, user_tier)

def render_certificate_gallery(certificates, user_tier):
    """Render certificates in gallery grid"""
    
    cols = st.columns(2)
    
    for idx, cert in enumerate(certificates):
        col = cols[idx % 2]
        
        with col:
            with st.container():
                # Certificate card
                st.image(
                    cert.png_url or cert.pdf_url,
                    use_column_width=True
                )
                
                st.subheader(cert.course_title)
                st.caption(f"Issued: {cert.issue_date.strftime('%B %d, %Y')}")
                st.caption(f"Grade: {cert.grade}%")
                
                # Skills badges
                if cert.skills:
                    st.write("**Skills:**")
                    skill_tags = " ".join([f"`{skill}`" for skill in cert.skills[:5]])
                    st.markdown(skill_tags)
                
                # Action buttons
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("👁️ View", key=f"view_{cert.certificate_id}"):
                        render_certificate_modal(cert, user_tier)
                
                with col_b:
                    if st.button("⬇️ Download", key=f"download_{cert.certificate_id}"):
                        download_certificate_dialog(cert, user_tier)
                
                with col_c:
                    if user_tier in ["intermediate", "advanced"]:
                        if st.button("🔗 Share", key=f"share_{cert.certificate_id}"):
                            share_certificate_dialog(cert, user_tier)
                    else:
                        st.button(
                            "🔒 Share",
                            disabled=True,
                            help="Upgrade to Intermediate to share certificates",
                            key=f"share_locked_{cert.certificate_id}"
                        )
                
                st.markdown("---")

def render_certificate_modal(cert, user_tier):
    """Show certificate in modal/fullscreen"""
    
    with st.expando("Certificate Details", expanded=True):
        # Full certificate preview
        st.image(cert.png_url or cert.pdf_url, use_column_width=True)
        
        # Details
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Student**: {cert.student_name}")
            st.write(f"**Course**: {cert.course_title}")
            st.write(f"**Issue Date**: {cert.issue_date.strftime('%B %d, %Y')}")
            st.write(f"**Grade**: {cert.grade}%")
        
        with col2:
            st.write(f"**Certificate ID**: `{cert.certificate_id}`")
            st.write(f"**Verification**: [Verify Certificate]({cert.verification_url})")
            
            if cert.blockchain_tx_id and user_tier == "advanced":
                st.write(f"**Blockchain**: ✅ Verified")
                st.caption(f"TX: `{cert.blockchain_tx_id[:16]}...`")

def download_certificate_dialog(cert, user_tier):
    """Download certificate in available formats"""
    
    st.subheader("Download Certificate")
    
    # Available formats based on tier
    formats = ["PDF"]
    
    if user_tier in ["intermediate", "advanced"]:
        formats.append("PNG")
    
    if user_tier == "advanced":
        formats.append("SVG")
    
    format_choice = st.selectbox("Format", formats)
    
    if st.button("Download"):
        cert_client = CertificationExamClient()
        file_bytes = await cert_client.download_certificate(
            cert.certificate_id,
            format_choice.lower()
        )
        
        st.download_button(
            label=f"💾 Download {format_choice}",
            data=file_bytes,
            file_name=f"certificate_{cert.certificate_id}.{format_choice.lower()}",
            mime=f"application/{format_choice.lower()}"
        )

def share_certificate_dialog(cert, user_tier):
    """Share certificate dialog (Intermediate/Advanced)"""
    
    st.subheader("Share Certificate")
    
    # LinkedIn integration
    st.write("**🔗 LinkedIn**")
    
    if user_tier == "advanced":
        # Auto-fill LinkedIn form
        linkedin_url = generate_linkedin_share_url(cert, auto_fill=True)
    else:
        # Basic LinkedIn share
        linkedin_url = generate_linkedin_share_url(cert, auto_fill=False)
    
    if st.button("Share on LinkedIn", type="primary"):
        st.markdown(f"[Open LinkedIn]({linkedin_url})")
    
    st.markdown("---")
    
    # Direct link
    st.write("**🔗 Direct Link**")
    st.code(cert.verification_url, language=None)
    
    if st.button("📋 Copy Link"):
        st.success("Link copied to clipboard!")
    
    st.markdown("---")
    
    # QR Code
    st.write("**📱 QR Code**")
    qr_code = generate_qr_code(cert.verification_url)
    st.image(qr_code, width=200)
    
    # Digital Wallet (Advanced tier only)
    if user_tier == "advanced":
        st.markdown("---")
        st.write("**📲 Add to Digital Wallet**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Apple Wallet"):
                wallet_pass = generate_apple_wallet_pass(cert)
                st.download_button(
                    "Download .pkpass",
                    wallet_pass,
                    f"certificate_{cert.certificate_id}.pkpass"
                )
        
        with col2:
            if st.button("Google Pay"):
                wallet_url = generate_google_pay_url(cert)
                st.markdown(f"[Add to Google Pay]({wallet_url})")
```

---

## LinkedIn Integration

### LinkedIn Share URL Generation

```python
# certificates/linkedin_integration.py

def generate_linkedin_share_url(cert: Certificate, auto_fill: bool = False) -> str:
    """
    Generate LinkedIn certificate sharing URL
    
    Args:
        cert: Certificate object
        auto_fill: Whether to auto-fill form (Advanced tier)
    """
    
    if auto_fill:
        # Advanced tier: Pre-fill LinkedIn form
        params = {
            "name": cert.course_title,
            "organizationId": "edguide-org-id",
            "issueYear": cert.issue_date.year,
            "issueMonth": cert.issue_date.month,
            "certUrl": cert.verification_url,
            "certId": cert.certificate_id
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        
        return f"https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME&{query_string}"
    
    else:
        # Intermediate tier: Basic share
        return f"https://www.linkedin.com/sharing/share-offsite/?url={cert.verification_url}"
```

---

## Blockchain Verification (Advanced Tier)

### Blockchain Certificate Storage

```python
# certificates/blockchain_verifier.py

class BlockchainCertificateVerifier:
    """
    Store certificate hashes on blockchain for immutable verification
    (Advanced tier only)
    """
    
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_RPC_URL))
        self.contract = self.web3.eth.contract(
            address=CERTIFICATE_CONTRACT_ADDRESS,
            abi=CERTIFICATE_CONTRACT_ABI
        )
    
    async def register_certificate(
        self,
        certificate_id: str,
        cert_hash: str,
        student_address: str
    ) -> str:
        """
        Register certificate on blockchain
        
        Returns:
            Transaction hash
        """
        
        # Create transaction
        tx = self.contract.functions.registerCertificate(
            certificate_id,
            cert_hash
        ).buildTransaction({
            'from': PLATFORM_WALLET_ADDRESS,
            'nonce': self.web3.eth.getTransactionCount(PLATFORM_WALLET_ADDRESS)
        })
        
        # Sign and send
        signed_tx = self.web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for confirmation
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return receipt.transactionHash.hex()
    
    async def verify_certificate(
        self,
        certificate_id: str,
        cert_hash: str
    ) -> dict:
        """
        Verify certificate against blockchain record
        
        Returns:
            {
                "valid": True,
                "block_number": 12345,
                "timestamp": 1234567890,
                "tx_hash": "0x..."
            }
        """
        
        # Query blockchain
        result = self.contract.functions.verifyCertificate(
            certificate_id,
            cert_hash
        ).call()
        
        return {
            "valid": result[0],
            "block_number": result[1],
            "timestamp": result[2],
            "tx_hash": result[3]
        }
```

---

## Digital Wallet Integration (Advanced Tier)

### Apple Wallet Pass Generation

```python
# certificates/wallet_integration.py

from wallet import Pass

def generate_apple_wallet_pass(cert: Certificate) -> bytes:
    """Generate Apple Wallet pass for certificate"""
    
    # Create pass
    pass_obj = Pass(
        passTypeIdentifier="pass.online.gai-observe.certificate",
        organizationName="EdGuide",
        teamIdentifier="TEAM_ID"
    )
    
    # Add certificate details
    pass_obj.description = f"Certificate: {cert.course_title}"
    pass_obj.logoText = "EdGuide"
    pass_obj.backgroundColor = "rgb(44, 62, 80)"
    pass_obj.foregroundColor = "rgb(255, 255, 255)"
    
    # Primary field
    pass_obj.addPrimaryField("name", cert.student_name, "Student")
    
    # Secondary fields
    pass_obj.addSecondaryField("course", cert.course_title, "Course")
    pass_obj.addSecondaryField("date", cert.issue_date.strftime("%B %d, %Y"), "Issued")
    
    # Auxiliary fields
    pass_obj.addAuxiliaryField("grade", f"{cert.grade}%", "Grade")
    pass_obj.addAuxiliaryField("id", cert.certificate_id, "Certificate ID")
    
    # Barcode (QR code for verification)
    pass_obj.addBarcode(
        message=cert.verification_url,
        format="PKBarcodeFormatQR",
        altText=cert.certificate_id
    )
    
    # Generate .pkpass file
    pass_bytes = pass_obj.create()
    
    return pass_bytes
```

---

## Certificate Verification Page

### Public Verification Page

```python
# ui/pages/verify_certificate.py

def render_verification_page(certificate_id: str):
    """Public page to verify certificate authenticity"""
    
    st.title("🔍 Certificate Verification")
    
    # Verify certificate
    cert_client = CertificationExamClient()
    verification = await cert_client.verify_certificate(certificate_id)
    
    if verification["valid"]:
        st.success("✅ This is a valid EdGuide certificate")
        
        # Display certificate details
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Student Name**")
            st.write(verification["student_name"])
            
            st.write("**Course**")
            st.write(verification["course"])
        
        with col2:
            st.write("**Issue Date**")
            st.write(verification["issue_date"])
            
            st.write("**Certificate ID**")
            st.code(certificate_id)
        
        # Blockchain verification (if available)
        if verification.get("blockchain_verified"):
            st.markdown("---")
            st.success("🔗 Blockchain Verified")
            st.caption(f"Transaction: {verification['blockchain_tx']}")
            st.caption("This certificate is registered on an immutable blockchain ledger")
    
    else:
        st.error("❌ Invalid Certificate")
        st.warning("This certificate ID was not found in our records.")
```

---

## Related Documentation

- [System Architecture](./ARCHITECTURE.md)
- [Feature Gating](./FEATURE_GATING.md)
- [Progress Tracking](./PROGRESS_TRACKING.md)
- [Integrations](./INTEGRATIONS.md)

---

**Last Updated**: January 2026  
**Platform**: EdGuide (gai-observe.online)  
**Version**: 1.0
