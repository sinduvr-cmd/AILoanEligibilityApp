"""
AI Loan Eligibility System
==========================
A transparent, rule-based customer loan eligibility evaluation platform built with
Python and Streamlit.

Demonstrates core Python programming constructs:
- Variables and constants
- Input controls and form submission
- Lists and collection handling
- Conditional branching: if, if-else, if-elif-else
- Iteration: for loops
- Reusable modular functions
- Purely local evaluation without external APIs or data persistence
"""

from typing import List, Tuple, Dict, Any
import streamlit as st

# ==============================================================================
# 1. Configurable Demonstration Constants
# ==============================================================================
MIN_CREDIT_SCORE: int = 300
MAX_CREDIT_SCORE: int = 900

# Credit Score Thresholds
CREDIT_SCORE_REJECT_THRESHOLD: int = 600    # Below 600: Reject
CREDIT_SCORE_APPROVE_THRESHOLD: int = 750   # Above 750: Approve (600 to 750: Review)

# Monthly Salary Risk Thresholds in INR
SALARY_HIGH_RISK_THRESHOLD: int = 30000     # Below 30,000: High Risk
SALARY_LOW_RISK_THRESHOLD: int = 70000      # Above 70,000: Low Risk (30,000 to 70,000: Medium Risk)

# Named Constant for Existing Loans Approval Threshold
MAX_ALLOWED_EXISTING_LOANS: int = 1         # Maximum existing loans permitted for automated approval


# ==============================================================================
# 2. Pure Business Logic & Reusable Evaluation Functions
# ==============================================================================

def format_inr(amount: int) -> str:
    """Format an integer amount into Indian Rupee (INR) representation."""
    str_amt = str(amount)
    if len(str_amt) <= 3:
        formatted = str_amt
    else:
        last_three = str_amt[-3:]
        remaining = str_amt[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted = ",".join(groups) + "," + last_three
    return f"₹{formatted}"


def validate_inputs(
    customer_name: str,
    monthly_salary: int,
    credit_score: int,
    existing_loans: int
) -> Tuple[bool, List[str]]:
    """
    Validate customer inputs using if statements.
    
    Rules:
    - Customer Name must not be empty or whitespace.
    - Monthly Salary must be greater than zero.
    - Credit Score must be between 300 and 900, inclusive.
    - Existing Loans must not be negative.
    
    Returns:
        Tuple containing a boolean validity status and a list of specific error messages.
    """
    validation_errors: List[str] = []

    # Check 1: Customer Name must not be empty or whitespace
    if not customer_name or not customer_name.strip():
        validation_errors.append("Customer Name must not be empty or consist solely of whitespace.")

    # Check 2: Monthly Salary must be greater than zero
    if monthly_salary <= 0:
        validation_errors.append("Monthly Salary must be greater than zero INR.")

    # Check 3: Credit Score must be between 300 and 900, inclusive
    if credit_score < MIN_CREDIT_SCORE or credit_score > MAX_CREDIT_SCORE:
        validation_errors.append(
            f"Credit Score must be between {MIN_CREDIT_SCORE} and {MAX_CREDIT_SCORE}, inclusive."
        )

    # Check 4: Existing Loans must not be negative
    if existing_loans < 0:
        validation_errors.append("Existing Loans must not be negative.")

    # Determine overall validity
    if len(validation_errors) == 0:
        is_valid = True
    else:
        is_valid = False

    return is_valid, validation_errors


def evaluate_credit_score(credit_score: int) -> str:
    """
    Evaluate credit score tier using if-elif-else logic.
    
    Rules:
    - Below 600: Reject
    - 600 through 750: Review
    - Above 750: Approve
    """
    if credit_score < CREDIT_SCORE_REJECT_THRESHOLD:
        credit_assessment = "Reject"
    elif credit_score <= CREDIT_SCORE_APPROVE_THRESHOLD:
        credit_assessment = "Review"
    else:
        credit_assessment = "Approve"

    return credit_assessment


def assess_salary_risk(monthly_salary: int) -> str:
    """
    Assess salary risk category using if-elif-else logic.
    
    Rules:
    - Below ₹30,000: High Risk
    - ₹30,000 through ₹70,000: Medium Risk
    - Above ₹70,000: Low Risk
    """
    if monthly_salary < SALARY_HIGH_RISK_THRESHOLD:
        salary_risk = "High Risk"
    elif monthly_salary <= SALARY_LOW_RISK_THRESHOLD:
        salary_risk = "Medium Risk"
    else:
        salary_risk = "Low Risk"

    return salary_risk


def generate_final_decision(
    credit_score: int,
    monthly_salary: int,
    existing_loans: int
) -> Dict[str, Any]:
    """
    Generate the overall loan eligibility decision and detailed explanation.
    
    Demonstration Assumptions:
    - Rejected: Credit Score below 600.
    - Approved: Credit Score above 750, Monthly Salary above ₹70,000,
                and Existing Loans no greater than 1 (MAX_ALLOWED_EXISTING_LOANS).
    - Manual Review Required: All other valid combinations.
    """
    # Demonstration rule branch 1: Rejected
    if credit_score < CREDIT_SCORE_REJECT_THRESHOLD:
        decision = "Rejected"
        status_category = "rejected"
        explanation = (
            f"Credit score ({credit_score}) falls below the minimum required demonstration "
            f"threshold of {CREDIT_SCORE_REJECT_THRESHOLD}. Automated screening results in immediate rejection."
        )

    # Demonstration rule branch 2: Approved
    elif (
        credit_score > CREDIT_SCORE_APPROVE_THRESHOLD
        and monthly_salary > SALARY_LOW_RISK_THRESHOLD
        and existing_loans <= MAX_ALLOWED_EXISTING_LOANS
    ):
        decision = "Approved"
        status_category = "approved"
        explanation = (
            f"Applicant satisfies all prime demonstration criteria: High credit score "
            f"({credit_score} > {CREDIT_SCORE_APPROVE_THRESHOLD}), robust monthly salary "
            f"({format_inr(monthly_salary)} > {format_inr(SALARY_LOW_RISK_THRESHOLD)}), and low debt exposure "
            f"({existing_loans} <= {MAX_ALLOWED_EXISTING_LOANS} existing loan)."
        )

    # Demonstration rule branch 3: Manual Review Required (all other combinations)
    else:
        decision = "Manual Review Required"
        status_category = "review"
        
        # Build explanatory points for human underwriters
        review_reasons = []
        if credit_score <= CREDIT_SCORE_APPROVE_THRESHOLD:
            review_reasons.append(
                f"Credit score ({credit_score}) is in the moderate bracket (<= {CREDIT_SCORE_APPROVE_THRESHOLD})"
            )
        if monthly_salary <= SALARY_LOW_RISK_THRESHOLD:
            review_reasons.append(
                f"Monthly salary ({format_inr(monthly_salary)}) is not in the prime tier (> {format_inr(SALARY_LOW_RISK_THRESHOLD)})"
            )
        if existing_loans > MAX_ALLOWED_EXISTING_LOANS:
            review_reasons.append(
                f"Existing loans count ({existing_loans}) exceeds the automated clearance limit ({MAX_ALLOWED_EXISTING_LOANS})"
            )

        reasons_summary = "; ".join(review_reasons)
        explanation = (
            f"The application does not meet all automated approval parameters: {reasons_summary}. "
            f"Rerouting to credit underwriting committee for comprehensive manual assessment."
        )

    return {
        "decision": decision,
        "status_category": status_category,
        "explanation": explanation
    }


# ==============================================================================
# 3. Streamlit User Interface Rendering
# ==============================================================================

def main():
    """Main Streamlit application execution function."""
    st.set_page_config(
        page_title="AI Loan Eligibility System",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom Navy, Teal & Neutral Color Palette Styling
    custom_css = """
    <style>
        /* Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Top Banner Styling */
        .hero-container {
            background: linear-gradient(135deg, #0b192c 0%, #1e3e62 50%, #001f3f 100%);
            border: 1px solid rgba(13, 148, 136, 0.3);
            border-radius: 16px;
            padding: 24px 30px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(11, 25, 44, 0.4);
            color: #ffffff;
        }
        .hero-title {
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .hero-badge {
            background: rgba(13, 148, 136, 0.25);
            border: 1px solid #14b8a6;
            color: #5eead4;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 4px 10px;
            border-radius: 9999px;
        }
        .hero-subtitle {
            color: #cbd5e1;
            font-size: 1.0rem;
            margin-top: 8px;
            margin-bottom: 0px;
            line-height: 1.5;
        }

        /* Section Card */
        .dashboard-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
        }
        .card-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Decision Banner Styles */
        .decision-banner {
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 22px;
            border-left: 8px solid;
        }
        .decision-approved {
            background: #ecfdf5;
            border-color: #10b981;
            color: #065f46;
        }
        .decision-rejected {
            background: #fef2f2;
            border-color: #ef4444;
            color: #991b1b;
        }
        .decision-review {
            background: #fffbeb;
            border-color: #f59e0b;
            color: #92400e;
        }
        .decision-heading {
            font-size: 1.45rem;
            font-weight: 800;
            margin: 0 0 6px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .decision-desc {
            font-size: 0.95rem;
            margin: 0;
            line-height: 1.55;
        }

        /* Metric Badges */
        .metric-pill {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.9rem;
        }
        .pill-green {
            background: #d1fae5;
            color: #065f46;
            border: 1px solid #a7f3d0;
        }
        .pill-red {
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }
        .pill-amber {
            background: #fef3c7;
            color: #92400e;
            border: 1px solid #fde68a;
        }
        .pill-teal {
            background: #ccfbf1;
            color: #0f766e;
            border: 1px solid #99f6e4;
        }

        /* Document item badge */
        .doc-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            color: #1e293b;
            padding: 6px 12px;
            border-radius: 8px;
            margin-right: 8px;
            margin-bottom: 8px;
            font-size: 0.88rem;
            font-weight: 600;
        }

        /* Note and Disclaimer box */
        .disclaimer-box {
            background: #f8fafc;
            border: 1px dashed #94a3b8;
            border-radius: 10px;
            padding: 12px 16px;
            color: #64748b;
            font-size: 0.83rem;
            line-height: 1.5;
            margin-top: 16px;
        }

        /* Button Styling */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
            color: #ffffff;
            font-weight: 700;
            font-size: 1.05rem;
            padding: 10px 24px;
            border-radius: 10px;
            border: none;
            width: 100%;
            box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
            box-shadow: 0 6px 16px rgba(13, 148, 136, 0.45);
            color: #ffffff;
            transform: translateY(-1px);
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Sidebar Controls & Presets
    # --------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### 🏛️ System Navigation")
        st.caption("AI Loan Eligibility Evaluation System")
        st.markdown("---")
        
        st.markdown("#### ⚡ Quick Preset Test Scenarios")
        st.caption("Load verified presets to inspect calculation behavior:")
        
        selected_preset = st.selectbox(
            "Select Test Profile",
            [
                "Custom Input",
                "Example Applicant: Rahul Sharma (Approval)",
                "Boundary Test: Low Credit Score (Reject)",
                "Boundary Test: Moderate Credit 600 (Review)",
                "Boundary Test: High Credit 780, High Debt (Review)",
                "Boundary Test: High Credit 751, Low Salary (Review)"
            ]
        )

        preset_name = ""
        preset_salary = 50000
        preset_credit = 700
        preset_loans = 0
        preset_docs = ["Aadhaar", "PAN"]

        if selected_preset == "Example Applicant: Rahul Sharma (Approval)":
            preset_name = "Rahul Sharma"
            preset_salary = 85000
            preset_credit = 780
            preset_loans = 1
            preset_docs = ["Aadhaar", "PAN", "Salary Slip"]
        elif selected_preset == "Boundary Test: Low Credit Score (Reject)":
            preset_name = "Anil Verma"
            preset_salary = 95000
            preset_credit = 599
            preset_loans = 0
            preset_docs = ["PAN", "Salary Slip"]
        elif selected_preset == "Boundary Test: Moderate Credit 600 (Review)":
            preset_name = "Pooja Patel"
            preset_salary = 75000
            preset_credit = 600
            preset_loans = 1
            preset_docs = ["Aadhaar", "PAN"]
        elif selected_preset == "Boundary Test: High Credit 780, High Debt (Review)":
            preset_name = "Karthik Iyer"
            preset_salary = 90000
            preset_credit = 780
            preset_loans = 2
            preset_docs = ["Aadhaar", "PAN", "Salary Slip"]
        elif selected_preset == "Boundary Test: High Credit 751, Low Salary (Review)":
            preset_name = "Sneha Kulkarni"
            preset_salary = 30000
            preset_credit = 751
            preset_loans = 0
            preset_docs = ["Aadhaar"]

        st.markdown("---")
        st.markdown("#### 📋 Demonstration Policy Rules")
        st.markdown(
            """
            - **Credit Assessment**:
              - `< 600`: `Reject`
              - `600 - 750`: `Review`
              - `> 750`: `Approve`
            - **Salary Risk Category**:
              - `< ₹30,000`: `High Risk`
              - `₹30,000 - ₹70,000`: `Medium Risk`
              - `> ₹70,000`: `Low Risk`
            - **Final Automated Decision**:
              - **Approved**: Credit > 750 AND Salary > ₹70,000 AND Existing Loans ≤ 1
              - **Rejected**: Credit < 600
              - **Manual Review Required**: All other combinations
            """
        )
        st.caption("🔒 Pure local processing. Zero data persistence.")

    # --------------------------------------------------------------------------
    # Hero Header Banner
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-title">
                <span>🏦 AI Loan Eligibility System</span>
                <span class="hero-badge">Algorithmic Engine</span>
            </div>
            <p class="hero-subtitle">
                Transparent, rule-based retail lending assessment with automated risk tiers,
                validation checks, and instant applicant profiling.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------------------------
    # Main Form & Dashboard Layout
    # --------------------------------------------------------------------------
    col_input, col_results = st.columns([1.05, 1.35], gap="large")

    # Left Column: Input Form
    with col_input:
        st.markdown(
            """
            <div class="card-title">
                <span>📝</span> Customer Information Form
            </div>
            """,
            unsafe_allow_html=True
        )
        st.caption("Enter customer details to perform transparent rule-based eligibility evaluation.")

        with st.form(key="loan_evaluation_form"):
            form_customer_name = st.text_input(
                "Customer Name *",
                value=preset_name,
                placeholder="e.g., Rahul Sharma",
                help="Enter the full name of the applicant. Must not be empty or whitespace."
            )

            form_monthly_salary = st.number_input(
                "Monthly Salary in INR *",
                min_value=0,
                max_value=10000000,
                value=preset_salary,
                step=5000,
                help="Gross monthly income in Indian Rupees. Must be greater than 0."
            )

            form_credit_score = st.number_input(
                "Credit Score *",
                min_value=0,
                max_value=1000,
                value=preset_credit,
                step=10,
                help="CIBIL or bureau credit score. Must be between 300 and 900 inclusive."
            )

            form_existing_loans = st.number_input(
                "Existing Loans *",
                min_value=0,
                max_value=100,
                value=preset_loans,
                step=1,
                help="Number of active loan accounts. Must be a non-negative integer."
            )

            form_documents_submitted = st.multiselect(
                "Documents Submitted",
                options=["Aadhaar", "PAN", "Salary Slip"],
                default=preset_docs,
                help="Select all verification documents submitted by the customer."
            )

            submit_button = st.form_submit_button(label="Evaluate Eligibility")

        st.markdown(
            """
            <div class="disclaimer-box">
                <strong>Privacy & Security Notice:</strong> This application collects document names only
                and does not request identity numbers or file uploads. No personal information is stored
                or persisted to databases or external services.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Right Column: Validation & Results Dashboard
    with col_results:
        st.markdown(
            """
            <div class="card-title">
                <span>📊</span> Assessment Dashboard & Audit
            </div>
            """,
            unsafe_allow_html=True
        )

        if submit_button:
            # 1. Validation
            is_valid, validation_errors = validate_inputs(
                customer_name=form_customer_name,
                monthly_salary=int(form_monthly_salary),
                credit_score=int(form_credit_score),
                existing_loans=int(form_existing_loans)
            )

            if not is_valid:
                st.error("⚠️ Input Validation Failed. Please correct the following errors:")
                for err_idx, error_message in enumerate(validation_errors, start=1):
                    st.markdown(f"- **Error {err_idx}:** {error_message}")
                st.info("Results are generated only when all input parameters pass validation.")
            else:
                clean_name = form_customer_name.strip()
                salary_int = int(form_monthly_salary)
                credit_int = int(form_credit_score)
                loans_int = int(form_existing_loans)
                
                # Store document selections in a Python list
                documents_list: List[str] = list(form_documents_submitted)

                # Evaluate credit score tier
                credit_assessment = evaluate_credit_score(credit_int)

                # Assess salary risk category
                salary_risk = assess_salary_risk(salary_int)

                # Generate final decision and explanation
                decision_result = generate_final_decision(
                    credit_score=credit_int,
                    monthly_salary=salary_int,
                    existing_loans=loans_int
                )

                final_decision = decision_result["decision"]
                status_category = decision_result["status_category"]
                decision_explanation = decision_result["explanation"]

                if status_category == "approved":
                    banner_class = "decision-approved"
                    status_icon = "✅"
                    status_label = "APPROVED"
                    status_subtext = "Instant Clearance Qualified"
                elif status_category == "rejected":
                    banner_class = "decision-rejected"
                    status_icon = "❌"
                    status_label = "REJECTED"
                    status_subtext = "Automatic Screening Criteria Not Met"
                else:
                    banner_class = "decision-review"
                    status_icon = "⚠️"
                    status_label = "MANUAL REVIEW REQUIRED"
                    status_subtext = "Referred to Credit Underwriter Review"

                decision_html = f"""
                <div class="decision-banner {banner_class}">
                    <div class="decision-heading">
                        <span>{status_icon}</span>
                        <span>{status_label}</span>
                    </div>
                    <div style="font-weight: 600; font-size: 0.9rem; margin-bottom: 8px; opacity: 0.9;">
                        {status_subtext}
                    </div>
                    <p class="decision-desc">
                        {decision_explanation}
                    </p>
                </div>
                """
                st.markdown(decision_html, unsafe_allow_html=True)

                st.markdown("#### 👤 Applicant Profile & Risk Tiers")
                
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.markdown(
                        f"""
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
                            <div style="font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Customer Name</div>
                            <div style="font-size: 1.15rem; color: #0f172a; font-weight: 700;">{clean_name}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    if credit_assessment == "Approve":
                        credit_pill = "pill-green"
                        credit_text = "Approve (Low Bureau Risk)"
                    elif credit_assessment == "Review":
                        credit_pill = "pill-amber"
                        credit_text = "Review (Moderate Risk)"
                    else:
                        credit_pill = "pill-red"
                        credit_text = "Reject (Elevated Risk)"

                    st.markdown(
                        f"""
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
                            <div style="font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Credit Assessment</div>
                            <div style="margin-top: 6px;">
                                <span class="metric-pill {credit_pill}">{credit_assessment}</span>
                            </div>
                            <div style="font-size: 0.82rem; color: #475569; margin-top: 4px;">Score: {credit_int} / 900 ({credit_text})</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px;">
                            <div style="font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Existing Loans</div>
                            <div style="font-size: 1.15rem; color: #0f172a; font-weight: 700;">{loans_int} active account(s)</div>
                            <div style="font-size: 0.82rem; color: #475569; margin-top: 2px;">
                                Approval threshold ceiling: &le; {MAX_ALLOWED_EXISTING_LOANS}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with m_col2:
                    formatted_salary_str = format_inr(salary_int)
                    st.markdown(
                        f"""
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
                            <div style="font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Monthly Salary (INR)</div>
                            <div style="font-size: 1.15rem; color: #0f172a; font-weight: 700;">{formatted_salary_str}</div>
                            <div style="font-size: 0.82rem; color: #475569; margin-top: 2px;">Annualized: {format_inr(salary_int * 12)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if salary_risk == "Low Risk":
                        sal_pill = "pill-green"
                    elif salary_risk == "Medium Risk":
                        sal_pill = "pill-amber"
                    else:
                        sal_pill = "pill-red"

                    st.markdown(
                        f"""
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
                            <div style="font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Salary Risk Category</div>
                            <div style="margin-top: 6px;">
                                <span class="metric-pill {sal_pill}">{salary_risk}</span>
                            </div>
                            <div style="font-size: 0.82rem; color: #475569; margin-top: 4px;">Tier classification based on monthly income</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Documents display with Python list and for loop
                    st.markdown(
                        """
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px;">
                            <div style="font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; margin-bottom: 6px;">Documents Submitted</div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    if len(documents_list) > 0:
                        docs_html = ""
                        for doc_item in documents_list:
                            docs_html += f'<span class="doc-badge">📄 {doc_item}</span>'
                        st.markdown(docs_html, unsafe_allow_html=True)
                    else:
                        st.markdown(
                            '<div style="color: #64748b; font-style: italic; font-size: 0.9rem;">No documents submitted</div>',
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <div class="disclaimer-box" style="margin-top: 20px;">
                        <strong>Demonstration Policy Rules Explanation:</strong>
                        <br>
                        • <strong>Automated Rejection:</strong> Triggered whenever Credit Score &lt; 600.<br>
                        • <strong>Automated Approval:</strong> Requires Credit Score &gt; 750 AND Monthly Salary &gt; ₹70,000 AND Existing Loans &le; {MAX_ALLOWED_EXISTING_LOANS}.<br>
                        • <strong>Manual Review:</strong> All other valid applicant profiles are routed for manual review.<br>
                        <em>Note: These demonstration rules represent transparent algorithmic logic for demonstration purposes and do not represent an actual commercial bank's lending policy.</em>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.info("👈 Enter applicant information on the left and click **'Evaluate Eligibility'** to generate the real-time assessment.")
            
            st.markdown(
                """
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; color: #334155;">
                    <h5 style="margin-top: 0; color: #0f172a;">How Eligibility is Evaluated:</h5>
                    <ol style="padding-left: 20px; margin-bottom: 0; line-height: 1.7; font-size: 0.92rem;">
                        <li><strong>Rigorous Input Validation:</strong> Name non-empty, salary &gt; 0, credit score in [300, 900], existing loans &ge; 0.</li>
                        <li><strong>Credit Tier Classification:</strong> Separately identifies Reject (&lt;600), Review (600–750), or Approve (&gt;750).</li>
                        <li><strong>Income Risk Grouping:</strong> Categorizes High Risk (&lt;₹30,000), Medium Risk (₹30,000–₹70,000), or Low Risk (&gt;₹70,000).</li>
                        <li><strong>Document Verification:</strong> Records presented identity & income documents via iterative list processing.</li>
                        <li><strong>Combined Final Decision:</strong> Generates instant approval, automated rejection, or specialist review.</li>
                    </ol>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 8px 0 16px 0;">
            <strong>AI Loan Eligibility System</strong> • Python & Streamlit • Pure Rule-Based Algorithmic Assessment
        </div>
        """,
        unsafe_allow_html=True
    )


# Run main application
if __name__ == "__main__":
    main()
