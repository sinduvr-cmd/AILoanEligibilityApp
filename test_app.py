"""
Unit and Boundary Verification Test Suite
=========================================
Tests for AI Loan Eligibility System core logic.
Verifies all boundary conditions, input validations, and demonstration rules.
"""

import unittest
from app import (
    validate_inputs,
    evaluate_credit_score,
    assess_salary_risk,
    generate_final_decision,
    format_inr,
    MIN_CREDIT_SCORE,
    MAX_CREDIT_SCORE,
    CREDIT_SCORE_REJECT_THRESHOLD,
    CREDIT_SCORE_APPROVE_THRESHOLD,
    SALARY_HIGH_RISK_THRESHOLD,
    SALARY_LOW_RISK_THRESHOLD,
    MAX_ALLOWED_EXISTING_LOANS
)


class TestAILoanEligibilitySystem(unittest.TestCase):

    # --------------------------------------------------------------------------
    # 1. Input Validation Tests
    # --------------------------------------------------------------------------
    def test_validation_empty_and_whitespace_name(self):
        """Test that empty or whitespace-only customer names are rejected."""
        valid, errors = validate_inputs("", 50000, 700, 0)
        self.assertFalse(valid)
        self.assertTrue(any("empty" in e.lower() for e in errors))

        valid, errors = validate_inputs("   \t  \n ", 50000, 700, 0)
        self.assertFalse(valid)
        self.assertTrue(any("whitespace" in e.lower() for e in errors))

    def test_validation_monthly_salary_must_be_positive(self):
        """Test that zero and negative monthly salaries are rejected."""
        valid, errors = validate_inputs("Anita", 0, 700, 0)
        self.assertFalse(valid)
        self.assertTrue(any("greater than zero" in e.lower() for e in errors))

        valid, errors = validate_inputs("Anita", -5000, 700, 0)
        self.assertFalse(valid)
        self.assertTrue(any("greater than zero" in e.lower() for e in errors))

    def test_validation_credit_score_range(self):
        """Test credit score boundaries (300 to 900 inclusive)."""
        # Lower invalid
        valid, errors = validate_inputs("Anita", 50000, 299, 0)
        self.assertFalse(valid)
        self.assertTrue(any("300 and 900" in e for e in errors))

        # Upper invalid
        valid, errors = validate_inputs("Anita", 50000, 901, 0)
        self.assertFalse(valid)
        self.assertTrue(any("300 and 900" in e for e in errors))

        # Valid boundaries
        valid, errors = validate_inputs("Anita", 50000, 300, 0)
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)

        valid, errors = validate_inputs("Anita", 50000, 900, 0)
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)

    def test_validation_existing_loans_non_negative(self):
        """Test that existing loans cannot be negative."""
        valid, errors = validate_inputs("Anita", 50000, 700, -1)
        self.assertFalse(valid)
        self.assertTrue(any("negative" in e.lower() for e in errors))

        valid, errors = validate_inputs("Anita", 50000, 700, 0)
        self.assertTrue(valid)

    def test_validation_multiple_simultaneous_errors(self):
        """Test that multiple validation errors are all captured."""
        valid, errors = validate_inputs("   ", 0, 250, -2)
        self.assertFalse(valid)
        self.assertEqual(len(errors), 4)

    # --------------------------------------------------------------------------
    # 2. Credit Score Assessment Tests
    # --------------------------------------------------------------------------
    def test_credit_score_boundaries(self):
        """
        Verify Credit Assessment boundary values:
        - 300: Reject
        - 599: Reject
        - 600: Review
        - 750: Review
        - 751: Approve
        - 900: Approve
        """
        self.assertEqual(evaluate_credit_score(300), "Reject")
        self.assertEqual(evaluate_credit_score(599), "Reject")
        self.assertEqual(evaluate_credit_score(600), "Review")
        self.assertEqual(evaluate_credit_score(750), "Review")
        self.assertEqual(evaluate_credit_score(751), "Approve")
        self.assertEqual(evaluate_credit_score(900), "Approve")

    # --------------------------------------------------------------------------
    # 3. Monthly Salary Risk Category Tests
    # --------------------------------------------------------------------------
    def test_salary_risk_boundaries(self):
        """
        Verify Salary Risk boundary values:
        - 29999: High Risk
        - 30000: Medium Risk
        - 70000: Medium Risk
        - 70001: Low Risk
        """
        self.assertEqual(assess_salary_risk(29999), "High Risk")
        self.assertEqual(assess_salary_risk(30000), "Medium Risk")
        self.assertEqual(assess_salary_risk(70000), "Medium Risk")
        self.assertEqual(assess_salary_risk(70001), "Low Risk")

    # --------------------------------------------------------------------------
    # 4. Final Decision Demonstration Rules Tests
    # --------------------------------------------------------------------------
    def test_specified_example_rahul_sharma(self):
        """
        Verify user-specified test example:
        Customer Name: Rahul Sharma
        Monthly Salary: 85000
        Credit Score: 780
        Existing Loans: 1
        Documents: Aadhaar, PAN, Salary Slip

        Expected:
        Credit Assessment: Approve
        Salary Risk Category: Low Risk
        Final Decision: Approved
        """
        credit_eval = evaluate_credit_score(780)
        salary_eval = assess_salary_risk(85000)
        decision_dict = generate_final_decision(
            credit_score=780,
            monthly_salary=85000,
            existing_loans=1
        )

        self.assertEqual(credit_eval, "Approve")
        self.assertEqual(salary_eval, "Low Risk")
        self.assertEqual(decision_dict["decision"], "Approved")
        self.assertEqual(decision_dict["status_category"], "approved")
        self.assertIn("Applicant satisfies all prime demonstration criteria", decision_dict["explanation"])

    def test_final_decision_rejections(self):
        """Credit score below 600 must be Rejected regardless of salary or loans."""
        # Low credit, very high salary, 0 loans
        res = generate_final_decision(credit_score=599, monthly_salary=200000, existing_loans=0)
        self.assertEqual(res["decision"], "Rejected")
        self.assertEqual(res["status_category"], "rejected")

        # Minimum score boundary 300
        res = generate_final_decision(credit_score=300, monthly_salary=150000, existing_loans=0)
        self.assertEqual(res["decision"], "Rejected")

    def test_final_decision_existing_loans_boundary(self):
        """
        Verify existing loan boundaries (0, 1, 2) when other metrics are prime:
        - 0 loans: Approved
        - 1 loan: Approved (threshold is <= 1)
        - 2 loans: Manual Review Required (> 1)
        """
        # 0 loans
        res_0 = generate_final_decision(credit_score=780, monthly_salary=85000, existing_loans=0)
        self.assertEqual(res_0["decision"], "Approved")

        # 1 loan
        res_1 = generate_final_decision(credit_score=780, monthly_salary=85000, existing_loans=1)
        self.assertEqual(res_1["decision"], "Approved")

        # 2 loans
        res_2 = generate_final_decision(credit_score=780, monthly_salary=85000, existing_loans=2)
        self.assertEqual(res_2["decision"], "Manual Review Required")
        self.assertEqual(res_2["status_category"], "review")

    def test_final_decision_manual_review_scenarios(self):
        """Test cases where profiles are valid but require human review."""
        # Credit in review zone (750), high salary, 0 loans
        res = generate_final_decision(credit_score=750, monthly_salary=85000, existing_loans=0)
        self.assertEqual(res["decision"], "Manual Review Required")

        # Credit in approve zone (751), salary exactly at threshold (70000), 0 loans
        res = generate_final_decision(credit_score=751, monthly_salary=70000, existing_loans=0)
        self.assertEqual(res["decision"], "Manual Review Required")

        # Credit in approve zone (751), salary just above threshold (70001), 0 loans -> Approved
        res = generate_final_decision(credit_score=751, monthly_salary=70001, existing_loans=0)
        self.assertEqual(res["decision"], "Approved")

    def test_currency_formatting(self):
        """Test formatting of Indian currency numbers."""
        self.assertEqual(format_inr(85000), "₹85,000")
        self.assertEqual(format_inr(100000), "₹1,00,000")
        self.assertEqual(format_inr(1250000), "₹12,50,000")
        self.assertEqual(format_inr(500), "₹500")


if __name__ == "__main__":
    unittest.main()
