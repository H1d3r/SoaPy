# Description
SOAPy is a Proof of Concept (PoC) utility for conducting offensive interaction with Active Directory Web Services (ADWS) through a SOCKS5 proxy.

SOAPy includes previously undeveloped custom python implementations of a collection of Microsoft protocols required for interaction with the ADWS service. This includes but is not limited to: NNS (.NET NegotiateStream Protocol), NMF (.NET Message Framing Protocol), and NBFSE (.NET Binary Format: SOAP Extension). 

<<<<<<< main
The protocol structure for interacting with ADWS is shown below:
![image](https://github.com/user-attachments/assets/e83a3e60-7aaf-4084-bcab-41e400d4055e)

The blog detailing the original research largely from an engineering perspective can be found [here](https://www.ibm.com/think/x-force/stealthy-enumeration-of-active-directory-environments-through-adws)

# Usage
```
███████╗ ██████╗  █████╗ ██████╗ ██╗   ██╗
██╔════╝██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
███████╗██║   ██║███████║██████╔╝ ╚████╔╝ 
╚════██║██║   ██║██╔══██║██╔═══╝   ╚██╔╝  
███████║╚██████╔╝██║  ██║██║        ██║   
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝        ╚═╝  

@_logangoins
github.com/jlevere

usage: soapy [-h] [--debug] [--ts] [-H nthash] [--users] [--computers]
             [--groups] [--constrained] [--unconstrained] [--spns]
             [--asreproastable] [--admins] [--rbcds] [-q query]
             [-f attr,attr,...] [-dn distinguishedname] [-p] [--rbcd source]
             [--spn value] [--asrep] [--account account] [--remove]
             [--addcomputer [MACHINE]] [--computer-pass pass] [--ou ou]
             [--delete-computer MACHINE] [--disable-account MACHINE]
             [--shadow-creds ACTION] [--shadow-target TARGET] [--device-id ID]
             [--cert-filename NAME] [--cert-export TYPE]
             [--cert-password PASS] [--shadow-creds-help] [--dns-add FQDN]
             [--dns-modify FQDN] [--dns-remove FQDN] [--dns-tombstone FQDN]
             [--dns-resurrect FQDN] [--dns-ip IP] [--ldapdelete]
             [--allow-multiple] [--ttl TTL] [--tcp]
             [connection]
=======
SOAPy started as a [research project at IBM X-Force Red with Jackson Leverett](https://www.ibm.com/think/x-force/stealthy-enumeration-of-active-directory-environments-through-adws) to rewrite the proprietary Microsoft .NET mechanisms/library that [FalconForce’s SOAPHound](https://falconforce.nl/soaphound-tool-to-collect-active-directory-data-via-adws/) uses to interact with ADWS, so recon and post-exploitation operations would be possible through a SOCKS5 proxy from Linux on Red Team assessments. After joining [SpecterOps](https://specterops.io), I decided to continue development on the project to bring it up to operational speed. 
>>>>>>> main

SOAPy is used for interacting with ADWS over a proxy for stealthy recon into an internal Active Directory environment. SOAPy is intended to be used as an ADWS ingestor for Active Directory, then the resultant data can be transformed to [BloodHound](https://specterops.io/bloodhound-community-edition/) compatible JSON using [Matt Creel’s BOFHound project](https://github.com/coffeegist/bofhound). The JSON transformed from BOFHound can then be uploaded into BloodHound for post-processing and visualization of attack paths.

SOAPy can also perform targeted post-exploitation operations in Active Directory, useful in many assessments when evasive LDAP write operations are required.

This includes the following tradecraft:

1. servicePrincipalName writing for targeted kerberoasting
2. userAccountControl writing for targeted AS-REProasting
3. msDs-AllowedToActOnBehalfOfOtherIdentity writing for Resource-Based Constrained Delegation (RBCD) attacks
4. msDs-KeyCredentialLink writing for Shadow Credentials attacks
5. DNS record additions for authentication coercion primitives

<<<<<<< main
Writing:
  --rbcd source         Write/remove RBCD (source computer)
  --spn value           Write servicePrincipalName value (use --remove to
                        delete)
  --asrep               Write DONT_REQ_PREAUTH flag (asrep roastable)
  --account account     Account to perform operations on
  --remove              Remove attribute value based on operation
  --addcomputer [MACHINE]
                        Create a computer account in AD
  --computer-pass pass  Password for the new computer account
  --ou ou               DN of the OU where to create the computer
  --delete-computer MACHINE
                        Delete an existing computer account
  --disable-account MACHINE
                        Disable a computer account
  --dns-add FQDN        Add A record (FQDN). Requires --dns-ip
  --dns-modify FQDN     Modify/replace A record (FQDN). Requires --dns-ip
  --dns-remove FQDN     Remove A record (FQDN). Requires --dns-ip unless
                        --ldapdelete
  --dns-tombstone FQDN  Tombstone a dnsNode
  --dns-resurrect FQDN  Resurrect a tombstoned dnsNode
  --dns-ip IP           IP used with dns add/modify/remove
  --ldapdelete          Use delete on dnsNode object
  --allow-multiple      Allow multiple A records when adding
  --ttl TTL             TTL for new A record (default 180)
  --tcp                 Use DNS over TCP when fetching SOA serial

Shadow Credentials (msDS-KeyCredentialLink):
  --shadow-creds ACTION
                        Shadow Credentials action: list, add, remove, clear,
                        info
  --shadow-target TARGET
                        Target account for Shadow Credentials operation
  --device-id ID        Device ID for remove/info actions
  --cert-filename NAME  Filename for certificate export (add action)
  --cert-export TYPE    Export type: PEM or PFX (default: PFX)
  --cert-password PASS  Password for PFX file (random if not set)
  --shadow-creds-help   Display detailed Shadow Credentials help and examples

```

# Installation
With `pipx`:
```
pipx install .
```
=======
The protocol structure for interacting with ADWS is shown below:
<img width="1376" height="768" alt="ADWS Protocol Diagram" src="https://github.com/user-attachments/assets/78442899-2e6c-4f72-97c4-ef0d68cf0b3b" />
>>>>>>> main


The blog detailing the original research largely from an engineering perspective can be found here:

[SOAPy: Stealthy enumeration of Active Directory environments through ADWS - IBM X-Force Red](https://www.ibm.com/think/x-force/stealthy-enumeration-of-active-directory-environments-through-adws)

A SpecterOps blog detailing new and modern operational guidance for ADWS tradecraft with SOAPy can be found here: 

[Make Sure to Use SOAP(y) – An Operators Guide to Stealthy AD Collection Using ADWS - SpecterOps](https://specterops.io/blog/2025/07/25/make-sure-to-use-soapy-an-operators-guide-to-stealthy-ad-collection-using-adws)



