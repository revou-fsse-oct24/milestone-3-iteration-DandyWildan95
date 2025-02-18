<<<<<<< HEAD
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/OEA-wQat)
=======
# Activity Diagrams Documentation

This README explains the purpose, key decisions, and processes represented in the **User Authentication** and **Transaction Handling** activity diagrams. These UML-compliant diagrams were created using draw.io to visualize workflows involving actors, decisions, and outcomes.

---

## **1. User Authentication Activity Diagram**

<img width="258" alt="User Authentication" src="https://github.com/user-attachments/assets/7aaffec4-fc75-4170-a125-c9e9e1342030" />



### **Purpose**
This diagram outlines the workflow for authenticating a user, including login, password verification, error handling, and token generation for successful logins.

### **Actors Involved**
- **User**: Initiates the login process.
- **Authentication Service**: Verifies credentials and manages token generation.

---

### **Key Processes**
1. **Login Initiation**: 
   - The user submits credentials (username/password).
2. **Password Verification**: 
   - The Authentication Service checks if the password matches stored records.
3. **Token Generation**: 
   - On success, a token is generated for session management.
4. **Error Handling**: 
   - Invalid credentials trigger an error message and retry logic.

### **Key Decisions**
- **Valid Password?**: 
  - If `Yes`, proceed to generate a token.
  - If `No`, display an error and prompt for retry.
- **Retry?**: 
  - If `Yes`, loop back to credential submission.
  - If `No`, terminate the process.

### **Outcomes**
- ✅ **Success**: User gains access (token generated).
- ❌ **Failure**: Process terminates after retry attempts.

---

## **2. Transaction Handling Activity Diagram**

<img width="204" alt="Transaction Authentication" src="https://github.com/user-attachments/assets/62fa8e31-0496-4aed-8fd0-67f9faceff52" />


### **Purpose**
This diagram visualizes the workflow for processing transactions, including balance verification, transaction completion, and history generation.

### **Actors Involved**
- **User**: Initiates the transaction.
- **Transaction Service**: Validates balances and processes transactions.

---

### **Key Processes**
1. **Transaction Initiation**: 
   - The user inputs transaction details (e.g., amount, recipient).
2. **Balance Verification**: 
   - The Transaction Service checks if the user’s account has sufficient funds.
3. **Transaction Completion**: 
   - On success, funds are transferred.
4. **History Generation**: 
   - A record is added to the transaction history.

### **Key Decisions**
- **Sufficient Balance?**: 
  - If `Yes`, complete the transaction.
  - If `No`, display an error and prompt for retry.
- **Retry?**: 
  - If `Yes`, loop back to transaction initiation.
  - If `No`, terminate the process.

### **Outcomes**
- ✅ **Success**: Transaction completed and history updated.
- ❌ **Failure**: Process terminates after retry attempts.

---

## **How to Use These Diagrams**
1. **System Design**: 
   - Clarify authentication and transaction logic during planning.
2. **Documentation**: 
   - Supplement technical specs for developers or stakeholders.
3. **Troubleshooting**: 
   - Identify failure points (e.g., invalid credentials, insufficient funds).
4. **Training**: 
   - Onboard teams on system workflows.

---

## **Key Takeaways**
- **Swimlanes**: Separate responsibilities between actors (User vs. Services).
- **Decision Nodes**: Represent critical branching logic (e.g., "Valid Password?").
- **Retry Loops**: Handle errors gracefully by allowing user retries.
- **UML Compliance**: Follows standards for clarity and interoperability.

---

## **Tools Used**
- **draw.io**: For creating UML-compliant diagrams with swimlanes and decision nodes.
- **Mermaid Syntax**: Optional text-based visualization (see [Mermaid Live Editor](https://mermaid.live)).

---

For feedback or updates, open an issue or contact the maintainers.  
>>>>>>> 0a797a6 (Initial commit)
