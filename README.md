HOSPITAL PATIENT ADMINISTRATION SYSTEM  

Master Specification & Architectural Blueprint 

Module: UFCFAF-30-3 - Development of Information Systems Project 

Target Submission: Portfolio (29/04/2027) & Presentation (May 2027) 

 

1. Executive Summary & Problem Domain Analysis 

The specialist hospital currently manages patient care from the first GP referral to treatments and follow ups using a mix of old systems, paper forms, emails, and phone calls. Many different teams are involved in this process, including Medical Secretaries, Booking Teams, Call Handlers, Clinical Nurses, Consultants, and the Finance Team. Because the current process is fragmented, the hospital faces three main problems: 

 

⚬ Hard to track progress: It is difficult to see exactly where a patient is in their treatment journey. 

 

⚬ Hidden delays: Managers cannot easily see when administrative or clinical tasks are falling behind. 

 

⚬ Poor record-keeping: There is no clear, unchangeable history of who made clinical or financial decisions. 

 

The new Hospital Patient Administration System (HPAS) will fix these issues by automating the workflow and keeping clear records. Most importantly, it will strictly separate clinical decisions, administrative tasks, and financial activities so that each team only does what they are allowed to do. 

 

 

 

 

1. Stakeholder & Actor Analysis 

 

To make the system work properly, HPAS separates responsibilities into four main roles: 

⚬ Clinical Staff (Consultants & Nurses): They are the only ones who can review referrals, approve treatments, decide on chemotherapy cycles, and sign off clinic letters. 

⚬ Administrative Staff (Secretaries & Booking Teams): They check if referral documents are complete, book appointments using external calendars, answer general phone calls, and monitor if letters are sent on time. 

⚬ Financial Staff (Finance Team): They check how the treatment will be paid for, process payments, handle situations where payments fail, and manage refunds. 

⚬ External Services: These are outside systems the hospital connects to, such as the external scheduling service, external letter/mailing service, and the external Payment Service Provider (PSP). 

 

 

1. Functional Requirements (FR) 

 

Functional Requirements define the specific behaviors, tasks, and processes the system must perform. They are categorized into 6 core modules. 

 

Module 1: Referral Management 

 

⚬ FR 1.1 - Receive Referrals: The system must be able to receive and securely store incoming patient referrals (and supporting documents) from external General Practitioners (GPs) or hospitals. 

 

⚬ FR 1.2 - Document Checking: The system must allow Medical Secretaries to check referrals for missing documents and request them from the referring organizations. 

 

⚬ FR 1.3 - System Block (Clinical Decisions): The system must strictly block Medical Secretaries from rejecting referrals or making any clinical assessments. 

 

⚬ FR 1.4 - Consultant Review: Once reviewed, the system must provide the Consultant with options to: 'Accept', 'Reject', 'Request More Info', or 'Redirect' the referral to another service. 

 

⚬ FR 1.5 - Decision Logging: The system must mandatorily record the Consultant's final decision, the exact reason for it, and the identity of the Consultant. 

 

Module 2: Appointments & Scheduling 

 

⚬ FR 2.1 - Authorized Bookings Only: The system must only allow a 'New Patient Appointment' to be booked if the patient's referral has been officially accepted by a Consultant. 

 

⚬ FR 2.2 - External Scheduling Integration: The system must connect with the hospital's External Scheduling API to book appointments based on clinical priority and requested timeframes. 

 

⚬ FR 2.3 - Patient Notifications: If an appointment is more than 2 weeks away, the system generates a letter. If it is within 2 weeks, the system must prompt admin staff to call the patient. All call attempts and outcomes must be logged. 

 

⚬ FR 2.4 - Anti-Silent Booking: If the external service cannot find an appointment within the doctor's requested timeframe, the system must block staff from silently booking a later date. Instead, it must automatically alert the Pathway Team. 

 

⚬ FR 2.5 - Absence Management (DNA): If a patient cancels or Does Not Attend (DNA), the system must log it and route the case to the clinical team to decide the next steps. 

 

 

 

 

 

Module 3: Treatment Management 

 

⚬ FR 3.1 - Treatment Requests: Consultants must be able to create a 'Treatment Booking Request' in the system, detailing the start date, number of cycles, and required resources. 

 

⚬ FR 3.2 - System Block (Unauthorized Treatments): The system must block administrative staff from processing any treatment request that lacks clinical approval. 

 

⚬ FR 3.3 - External Service Outages: If external labs or treatment services are temporarily down, the system must keep the request as 'Pending', notify the team, and prevent the creation of duplicate appointments. 

 

⚬ FR 3.4 - Treatment Modifications: Any changes to a treatment plan must be approved by a doctor in the system. If the change impacts billing, the system must automatically notify the Finance Team. 

 

Module 4: Finance & Payment 

 

⚬ FR 4.1 - Funding Source: The Finance Team must be able to record who is funding the treatment (e.g., hospital, insurance, or patient) and input authorization reference numbers. 

 

⚬ FR 4.2 - Secure Payment Gateway: The system must securely connect to an external Payment Gateway to process patient payments. The system must NEVER store full credit card details. 

 

⚬ FR 4.3 - System Block (Pending Payments): The system must block the confirmation of standard treatment appointments until the payment is successfully completed. 

 

⚬ FR 4.4 - Clinical Overrides (Emergencies): In life-threatening emergencies, the system must allow clinical staff to bypass payment blocks to treat the patient immediately. The system will automatically notify Finance to resolve the payment later. 

 

⚬ FR 4.5 - Communication Failure Recovery: If a payment is taken but the receipt is lost due to a network error, the system must mark it as "Flagged for Investigation" and prevent the patient from being charged a second time. 

 

⚬ FR 4.6 - Refunds: Refund requests for cancelled treatments can only be submitted through the system by authorized Finance officers. 

 

Module 5: Inquiry & Call Handling 

 

⚬ FR 5.1 - Inquiry Logging: Every incoming inquiry must be logged with the time received, handler's name, routed team, response given, and 'Resolved' status. 

 

⚬ FR 5.2 - Call Routing: Call handlers must be blocked from giving medical advice. The system must route clinical questions to the Nurse Team and financial questions to the Finance Team. 

 

⚬ FR 5.3 - High Priority Flags: The system must allow users to flag urgent clinical inquiries for immediate attention. 

 

Module 6: Clinic Letters & Monitoring 

 

⚬ FR 6.1 - Drafting Letters: Consultants must be able to draft, select recipients, and approve Clinic Letters directly in the system after a consultation. 

 

⚬ FR 6.2 - Editing Restrictions: Administrative staff can only access the letter to fix formatting or typing errors; the system must block them from changing the clinical content. 

 

⚬ FR 6.3 - Date Tracking: The system must track the appointment date, drafted date, approved date, and sent date for every letter. 

 

⚬ FR 6.4 - Automated Reminders: If a letter is not approved within 7 days, the system must send automated reminders to the Consultant. 

 

⚬ FR 6.5 - Escalation Matrix: If a letter is delayed by 1 month, the system automatically notifies the Manager. At 3 months, it notifies Senior Management. Reminders must stop once the letter is approved. 

 

2. Non-Functional Requirements (NFR) 

 

Non-Functional Requirements define system attributes such as security, reliability, performance, and usability. 

 

⚬ NFR 1 - Security & Access Control: The system must use strictly enforced Role-Based Access Control. Logical boundaries must ensure clinical staff cannot process finances, and administrative staff cannot make clinical decisions. 

 

⚬ NFR 2 - Auditability (Audit Trail): Every action (viewing, editing, approving) must be recorded in an immutable Audit Trail with the user's ID, date, and time. Standard users cannot delete or edit these logs. 

 

⚬ NFR 3 - Data Integrity: Because data comes from multiple external systems, the system must use strict Identity Matching algorithms to prevent medical records from being attached to the wrong patient. 

 

⚬ NFR 4 - Usability (Frictionless UI): The user interface for clinical staff must be fast and require minimal data entry (frictionless) so that doctors do not waste valuable patient-care time on administrative clicks. 

 

⚬ NFR 5 - Reliability & Offline Continuity: The system must not crash if an external API (like scheduling or payments) goes offline. It must allow manual actions to be recorded and safely synced once the network is restored. 

 

⚬ NFR 6 - Accessibility & Communications: The system must store patient communication preferences (postal, digital, translation needed) and ensure external mailing services use the correct format. 

 

⚬ NFR 7 - Reporting & Analytics: The system must generate real-time reports for management, highlighting referral volumes, delays, unresolved inquiries, and financial bottlenecks. 

 
