## Challenges To Solve
* **Lack of Python Support:**

     Many vendors allow automation from their equipment, but this support is often limited to technologies such as syslog, snmp, or URL POST/GET.
*  **Certificate Spread:**

     Certificate based authentication management and security can be a challenge as certficates become spread across and enterprise with each new deployment.  A couple of the problems this often causes in operations are:
            
    1. **Certificate Mismatch**
    
        Certificates are deployed with a fire and forget mindset.  The trouble occurs when certificates are reissued.  Typically there is no way to track clients that are using the original certificate.   
    2. **Outdated Certificates**
    
        Clients using certificates are a challenge for operations to track therefore they will use the original certificate and never reissue certificates.
* **Wrapper Services**
    While building a wrapper is a fine work around, it creates an operational challenge because it has to be maintained in tandem to the code being wrapped.  These types of services are easily forgotten upon upgrades.  Specifically to creater of Cuckoo said please do not create wrapper.
