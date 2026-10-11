# AI Loan Eligibility System 🏦

A transparent, rule-based retail lending evaluation web application built with **Python** and **Streamlit**.

The application evaluates customer loan eligibility using transparent, rule-based logic without opaque black-box models or third-party external dependencies.

---

## 📌 Repository Information & Git Path

- **Git Repository URL**: [https://github.com/sinduvr-cmd/AILoanEligibilityApp](https://github.com/sinduvr-cmd/AILoanEligibilityApp)
- **Git User Profile**: [https://github.com/sinduvr-cmd](https://github.com/sinduvr-cmd)

---

## 🚀 Quickstart & Setup Instructions

### 1. Prerequisites
- Python 3.9+ (tested through Python 3.14)
- Web browser (Chrome, Firefox, Safari, Edge)

### 2. Installation
Clone the repository or navigate to the project directory:

```bash
git clone https://github.com/sinduvr-cmd/AILoanEligibilityApp.git
cd AILoanEligibilityApp
```

Create and activate an isolated virtual environment (recommended):

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the Application
Execute the standard Streamlit launch command:

```bash
streamlit run app.py
```

Once started, access the dashboard in your web browser at:
`http://localhost:8501`

### 4. Run Automated Unit Tests
To run the full suite of automated unit and boundary tests:

```bash
python -m unittest -v test_app.py
```

---

## ⚙️ Demonstration Assumptions & Evaluation Rules

The system implements configurable demonstration screening rules separated into modular Python functions and named constants.

> **Important Demonstration Disclaimer:**  
> These rules and thresholds are demonstration assumptions designed for algorithmic educational assessment. They do not represent an actual commercial bank's official lending policy.

### Core Named Constants
```python
MIN_CREDIT_SCORE = 300
MAX_CREDIT_SCORE = 900

CREDIT_SCORE_REJECT_THRESHOLD = 600   # Below 600: Reject
CREDIT_SCORE_APPROVE_THRESHOLD = 750  # Above 750: Approve

SALARY_HIGH_RISK_THRESHOLD = 30000    # Below 30,000: High Risk
SALARY_LOW_RISK_THRESHOLD = 70000     # Above 70,000: Low Risk

MAX_ALLOWED_EXISTING_LOANS = 1        # Named constant threshold for automated clearance
```

---

### Step-by-Step Evaluation Workflow

#### 1. Input Collection
The input form collects:
- **Customer Name**: Text input
- **Monthly Salary in INR**: Integer input
- **Credit Score**: Integer input (300 to 900)
- **Existing Loans**: Non-negative integer input
- **Documents Submitted**: Multi-select control (`Aadhaar`, `PAN`, `Salary Slip`)
- **Evaluate Eligibility**: Form submit button

#### 2. Input Validation (`validate_inputs`)
Defensive conditional checks verify that:
- Customer Name is non-empty and does not contain solely whitespace.
- Monthly Salary is strictly greater than zero.
- Credit Score is between 300 and 900 inclusive.
- Existing Loans is not negative (&ge; 0).

Specific error messages are shown for each failed condition, and evaluations are computed only when all inputs pass validation.

#### 3. Credit Assessment (`evaluate_credit_score`)
Evaluated via `if-elif-else`:
- **Below 600**: `Reject`
- **600 through 750**: `Review`
- **Above 750**: `Approve`

#### 4. Salary Risk Assessment (`assess_salary_risk`)
Evaluated via `if-elif-else`:
- **Below ₹30,000**: `High Risk`
- **₹30,000 through ₹70,000**: `Medium Risk`
- **Above ₹70,000**: `Low Risk`

#### 5. Submitted Documents Processing
- Selections are stored in a Python list.
- A Python `for` loop iterates through the list to display each submitted document badge.
- When no documents are selected, the system displays `"No documents submitted"`.
- Collects document names only; never requests identity numbers or file uploads.

#### 6. Combined Final Decision (`generate_final_decision`)
Evaluated using the demonstration criteria:
- **Rejected**: Credit Score below 600.
- **Approved**: Credit Score above 750, Monthly Salary above ₹70,000, and Existing Loans no greater than 1 (`MAX_ALLOWED_EXISTING_LOANS`).
- **Manual Review Required**: In all other valid profile combinations.

---

## 📊 Results Dashboard & Visual Standards

The results dashboard incorporates:
- **Customer Name**
- **Monthly Salary** formatted cleanly in INR (e.g., `₹85,000`)
- **Credit Score** and out-of-900 benchmark
- **Existing Loans** count and active threshold limit
- **Credit Assessment** displayed separately
- **Salary Risk Category** displayed separately
- **Documents Submitted** list display via iteration
- **Final Decision** banner and plain-language explanation

### Color Palette & Accessibility
- **Approved**: Green banner (`#10b981`), green badge, with text label `APPROVED`.
- **Rejected**: Red banner (`#ef4444`), red badge, with text label `REJECTED`.
- **Manual Review Required**: Amber banner (`#f59e0b`), amber badge, with text label `MANUAL REVIEW REQUIRED`.
- Text labels always accompany colors to guarantee complete accessibility.

---

## 🧪 Verification & Boundary Value Testing

The application and test suite verify all critical boundary values:

| Dimension | Boundary Values Tested | Expected System Response | Status |
|:---|:---|:---|:---:|
| **Credit Score** | `300` | Minimum score boundary: `Reject` | ✅ Pass |
| **Credit Score** | `599` | Reject ceiling: `Reject` | ✅ Pass |
| **Credit Score** | `600` | Review floor: `Review` | ✅ Pass |
| **Credit Score** | `750` | Review ceiling: `Review` | ✅ Pass |
| **Credit Score** | `751` | Approve floor: `Approve` | ✅ Pass |
| **Credit Score** | `900` | Maximum score boundary: `Approve` | ✅ Pass |
| **Monthly Salary** | `₹29,999` | High Risk ceiling: `High Risk` | ✅ Pass |
| **Monthly Salary** | `₹30,000` | Medium Risk floor: `Medium Risk` | ✅ Pass |
| **Monthly Salary** | `₹70,000` | Medium Risk ceiling: `Medium Risk` | ✅ Pass |
| **Monthly Salary** | `₹70,001` | Low Risk floor: `Low Risk` | ✅ Pass |
| **Existing Loans** | `0` | Automated clearance eligible (`Approved`) | ✅ Pass |
| **Existing Loans** | `1` | Ceiling for automated clearance (`Approved`) | ✅ Pass |
| **Existing Loans** | `2` | Exceeds ceiling (`Manual Review Required`) | ✅ Pass |

### Verified Reference Example: Rahul Sharma
- **Customer Name**: `Rahul Sharma`
- **Monthly Salary**: `85000`
- **Credit Score**: `780`
- **Existing Loans**: `1`
- **Documents Submitted**: `Aadhaar`, `PAN`, `Salary Slip`

**Evaluation Outcome**:
- **Credit Assessment**: `Approve`
- **Salary Risk Category**: `Low Risk`
- **Final Decision**: `Approved`
- **Explanation**: Confirms credit score &gt; 750, salary &gt; ₹70,000, and existing loans &le; 1.

---

## 🏗️ Python Language Constructs Demonstrated

This project explicitly demonstrates core foundational Python programming constructs:
- **Variables & Data Types**: Strings, integers, booleans, and tuples.
- **Named Constants**: Global uppercase configuration constants.
- **Input Controls**: Streamlit form fields (`text_input`, `number_input`, `multiselect`, `form_submit_button`).
- **Lists**: Dynamic document collections and error queues.
- **Conditionals**:
  - `if` statements for defensive validation.
  - `if-else` branching for document rendering states.
  - `if-elif-else` ladder for credit tiers, salary risk, and final decisions.
- **Loops**: `for` loop iterations for displaying documents and validation errors.
- **Modular Functions**: Reusable functions with type annotations and docstrings.
- **Zero Persistence**: Strictly in-memory calculations without database or file persistence.
