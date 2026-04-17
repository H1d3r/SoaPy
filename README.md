# Description
SOAPy is a Proof of Concept (PoC) utility for conducting offensive interaction with Active Directory Web Services (ADWS) through a SOCKS5 proxy.

SOAPy includes previously undeveloped custom python implementations of a collection of Microsoft protocols required for interaction with the ADWS service. This includes but is not limited to: NNS (.NET NegotiateStream Protocol), NMF (.NET Message Framing Protocol), and NBFSE (.NET Binary Format: SOAP Extension). 

SOAPy started as a [research project at IBM X-Force Red with Jackson Leverett](https://www.ibm.com/think/x-force/stealthy-enumeration-of-active-directory-environments-through-adws) to rewrite the proprietary .NET mechanisms that [FalconForce’s SOAPHound](https://falconforce.nl/soaphound-tool-to-collect-active-directory-data-via-adws/) uses to interact with ADWS, so recon and post-exploitation operations would be possible through a SOCKS5 proxy from Linux on Red Team assessments. After joining [SpecterOps](https://specterops.io), I decided to continue development on the project to bring it up to operational speed. 

SOAPy is used for interacting with ADWS over a proxy for stealthy recon into an internal Active Directory environment. SOAPy can also perform targeted post-exploitation operations on LDAP, useful in many assessments when evasive LDAP write operations are required.

This includes the following tradecraft:

1. servicePrincipalName writing for targeted kerberoasting
2. userAccountControl writing for targeted AS-REProasting
3. msDs-AllowedToActOnBehalfOfOtherIdentity writing for Resource-Based Constrained Delegation (RBCD) attacks
4. msDs-KeyCredentialLink writing for Shadow Credentials attacks
5. DNS record additions for authentication coercion primitives

The protocol structure for interacting with ADWS is shown below:
<img width="1376" height="768" alt="ADWS Protocol Diagram" src="https://github.com/user-attachments/assets/78442899-2e6c-4f72-97c4-ef0d68cf0b3b" />


The blog detailing the original research largely from an engineering perspective can be found here:

[SOAPy: Stealthy enumeration of Active Directory environments through ADWS - IBM X-Force Red](https://www.ibm.com/think/x-force/stealthy-enumeration-of-active-directory-environments-through-adws)

A SpecterOps blog detailing new and modern operational guidance for ADWS tradecraft with SOAPy can be found here: 

[Make Sure to Use SOAP(y) – An Operators Guide to Stealthy AD Collection Using ADWS - SpecterOps](https://specterops.io/blog/2025/07/25/make-sure-to-use-soapy-an-operators-guide-to-stealthy-ad-collection-using-adws)



