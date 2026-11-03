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

⚬ Call Handling Team: They answer patient phone calls, book the first appointments, search for patient details, and pass medical questions to the nurses.

⚬ Treatment Booking Team: They schedule complex treatments (like chemotherapy) and make sure clinic rooms and equipment are available.

 

 

1. Functional Requirements (FR) 

 

Functional Requirements define the specific behaviors, tasks, and processes the system must perform. They are categorized into 6 core modules. 

 

Module 1: Referral Management

FR 1.1 - Receive Referrals

Description: The system must safely receive and save patient referrals and attached documents from GPs.

Expected Behavior: The system automatically creates a unique 'Referral ID', secures the documents, and puts the referral in the 'New Referrals' list.

Inputs: Patient details, GP details, PDF/Word documents.

Outputs: A new Referral ID and a 'Pending Review' status.

FR 1.2 - Document Checking

Description: Medical Secretaries need to check if the referral has all the necessary documents.

Expected Behavior: The user ticks a checklist on the screen. If documents are missing, the system automatically sends a request back to the GP.

Inputs: Secretary clicking the checklist.

Outputs: The status changes to 'Incomplete' or 'Ready for Clinical Review'.

FR 1.3 - System Block (Clinical Decisions)

Description: The system must stop Medical Secretaries from rejecting referrals or making medical decisions.

Expected Behavior: The buttons for 'Reject' or 'Assess' are completely hidden from users who have an 'Admin' role.

Exception Handling: If someone tries to force this using an API, the system will return a '403 Forbidden' error.

FR 1.4 - Consultant Review & FR 1.5 - Decision Logging

Description: Consultants must review the ready referrals, make a decision, and the system must save this decision permanently.

Expected Behavior: The Consultant chooses 'Accept', 'Reject', or 'Redirect'. The system forces them to type a 'Reason' before they can click save.

Inputs: Their decision (Accept/Reject), the typed reason, and the Consultant's User ID.

Outputs: A permanent log entry and the status changes to 'Accepted' or 'Rejected'.



Module 2: Appointments & Scheduling


FR 2.1 - Authorized Bookings Only & FR 2.2 - External Integration

Description: Call Handlers can only book appointments for referrals that a Consultant has accepted. They will use the hospital's external calendar system for this.

Expected Behavior: The system checks the external calendar for free times. If the patient's referral is not 'Accepted', the search button will not work.

Inputs: The preferred dates and the type of clinic.

Outputs: A list of free times and a Booking Confirmation ID.

FR 2.3 - Patient Notifications & FR 2.4 - Anti-Silent Booking

Description: The system automatically manages patient messages based on appointment dates and stops staff from picking dates the doctor didn't allow.

Expected Behavior: If the appointment is more than 14 days away, the system sends data to the external mailing service to post a letter. If it's less than 14 days, it tells the admin staff on their dashboard to call the patient. If the calendar has no free slots in the doctor's requested time, the system stops the booking and warns the Pathway Team.

Outputs: Data sent to the mailing service, or an alert on the screen.

FR 2.5 - Absence Management (DNA)

Description: The system records when patients cancel or don't show up.

Expected Behavior: When a Call Handler clicks 'DNA' (Did Not Attend), the system automatically sends the patient's file back to the Consultant to decide what to do next.


Module 3: Treatment Management


FR 3.1 - Treatment Requests & FR 3.2 - System Block

Description: Consultants create the treatment plans. Admins cannot process any plan that a doctor hasn't approved.

Expected Behavior: The Consultant enters the number of treatment cycles. The system creates a 'Treatment ID' showing 'Awaiting Booking'. Admin users are blocked from changing any medical details.

FR 3.3 - External Service Outages

Description: Stops data from getting lost if the outside lab or booking systems go down.

Expected Behavior: If the outside system doesn't respond (503 error), our system changes the status to 'Pending External Sync' and tries again automatically every 15 minutes.

FR 3.4 - Treatment Modifications

Description: If a doctor changes a treatment that affects the price, the system must tell the Finance team.

Expected Behavior: If a Consultant adds another treatment cycle, the system automatically sends a message (webhook) to the Finance Module to update the bill.

Module 4: Finance & Payment


FR 4.1 - Funding Source & FR 4.2 - Secure Payment Gateway

Description: The system connects to an outside Payment Service Provider (PSP) to take patient payments securely, following standard security rules.

Expected Behavior: The system sends the user to the PSP's secure payment page. Our HPAS system only gets back a secure 'Token' and a 'Success/Fail' message. It NEVER saves the actual credit card numbers.

Inputs: The Treatment ID and the amount to pay.

Outputs: A secure payment token and the payment status.

FR 4.3 - System Block & FR 4.4 - Clinical Overrides (Emergencies)

Description: The system stops treatments from being booked until they are paid for, unless it is a medical emergency.

Expected Behavior: Normally, you can't book if the status is not 'Paid'. But if a Consultant clicks 'Clinical Override', the system ignores the payment block, books the appointment, and sends a 'Debt Recovery' warning to the Finance team.

Inputs: The Consultant's override approval (they have to log in again to confirm).

FR 4.5 - Communication Failure Recovery

Description: This handles situations where money is taken from the patient's card, but the internet drops before the system gets the receipt.

Expected Behavior: The system asks the PSP if the payment worked. If it doesn't know, it marks the transaction as MARKED_FOR_INVESTIGATION so the Finance Team can check it manually. This stops the patient from being charged twice.

FR 4.6 - Refunds

Description: Only allowed Finance staff can use the system to process refunds for cancelled treatments.


Module 5: Inquiry & Call Handling


FR 5.1 - Inquiry Logging & FR 5.2 - Call Routing

Description: Every phone call is recorded, and questions are sent to the right team.

Expected Behavior: The Call Handler types in the call details. If the patient asks a medical question, the handler clicks 'Route to Clinical', and a warning pops up on the Nurse Team's screen.

FR 5.3 - High Priority Flags

Expected Behavior: There is an 'Urgent' checkbox. If ticked, the message turns red on the dashboard so it gets looked at immediately.


Module 6: Clinic Letters & Monitoring



FR 6.1 - Drafting & FR 6.2 - Editing Restrictions

Description: Consultants write the letters; Admins can only fix spelling or layout mistakes.

Expected Behavior: In the text editor, the 'Clinical Findings' box is locked so Admins can't type in it, but they can edit the patient's address and name.

FR 6.3 - Date Tracking, FR 6.4 - Reminders, & FR 6.5 - Escalation

Description: The system tracks dates and automatically warns people if letters are delayed.

Expected Behavior: The system runs a check every day. If a letter was drafted more than 7 days ago but not approved, it sends an alert to the Consultant. If it takes more than 30 days, it warns the Manager. If it hits 90 days, it warns Senior Management.
 


2. Non-Functional Requirements (NFR) 

 

Non-Functional Requirements define system attributes such as security, reliability, performance, and usability. 

 

⚬ NFR 1 - Security & Access Control: The system must use strictly enforced Role-Based Access Control. Logical boundaries must ensure clinical staff cannot process finances, and administrative staff cannot make clinical decisions. 

 

⚬ NFR 2 - Auditability (Audit Trail): Every action (viewing, editing, approving) must be recorded in an immutable Audit Trail with the user's ID, date, and time. Standard users cannot delete or edit these logs. 

 

⚬ NFR 3 - Data Integrity: Because data comes from multiple external systems, the system must use strict Identity Matching algorithms to prevent medical records from being attached to the wrong patient. 

 

⚬ NFR 4 - Usability (Frictionless UI): The user interface for clinical staff must be fast and require minimal data entry (frictionless) so that doctors do not waste valuable patient-care time on administrative clicks. 

 

⚬ NFR 5 - Reliability & Offline Continuity: The system must not crash if an external API (like scheduling or payments) goes offline. It must allow manual actions to be recorded and safely synced once the network is restored. 

 

⚬ NFR 6 - Accessibility & Communications: The system must store patient communication preferences (postal, digital, translation needed) and ensure external mailing services use the correct format. 

 

⚬ NFR 7 - Reporting & Analytics: The system must generate real-time reports for management, highlighting referral volumes, delays, unresolved inquiries, and financial bottlenecks. 

 
