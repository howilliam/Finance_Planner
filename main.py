# find the better from paying student finance off earlier or putting it in the stock market
# def calculate_years_to_payoff_sfe(
#     loan_amount, interest_rate, monthly_payment, write_off_years
# ):
def calculate_years_to_payoff_sfe(
    loan_amount: float,
    interest_rate: float,
    salary: float,
    write_off_years: int,
    optional_extra_payment=0,
) -> float:
    months = 0
    monthly_interest_rate = interest_rate / 100 / 12
    while loan_amount > 0:
        if months // 12 == 0:
            salary = salary * 1.03  # assuming a 3% salary increase every year
        monthly_payment = calculate_sfe_contributions(salary) + optional_extra_payment
        loan_amount = loan_amount * (1 + monthly_interest_rate) - monthly_payment
        months += 1
        if months / 12 > write_off_years:
            return write_off_years
    return months / 12


def calculate_investment_growth(
    initial_investment, monthly_return_rate, years, monthly_contribution=0
):
    total_investment = initial_investment
    for month in range(int(12 * years)):
        total_investment += monthly_contribution
        total_investment *= 1 + monthly_return_rate / 100 / 12

    return total_investment


# scenario 1, don't choose to pay off SFE early, just use default payment which is 9% above £27,295
# scenario 2, pay off SFE early using all disposable income, and invest nothing
# scenario 3, pay off SFE early using some disposable income, and invest the rest
# goal in general is to find out if you would have more money before or after paying off the loan


def compare_strategies(
    salary,
    loan_amount,
    interest_rate,
    monthly_payment,
    write_off_years,
    disposable_income,
    annual_return_rate,
):
    """
    Compares different strategies for paying off student loans versus investing.
    Strategies:
    1. Pay off student loans early using all disposable income.
    2. Invest all disposable income without paying off student loans early.
    param disposable_income: Post tax amount of money where person will choose to either pay off SFE or invest
    Returns a comparison of final amounts for each strategy.
    """

    # first understand if person will pay off loans early or not
    # basic simple scenario 1 where they don't pay anything extra just their salary amount
    auto_monthly_payment = calculate_sfe_contributions(
        salary
    )  # the default amount done by HMRC
    years_to_payoff = calculate_years_to_payoff_sfe(
        loan_amount, interest_rate, salary, write_off_years
    )
    print(f"Years to payoff SFE with auto payment: {years_to_payoff:.2f} years")
    investment_if_no_extra_payment = calculate_investment_growth(
        0, annual_return_rate, write_off_years, monthly_contribution=disposable_income
    )
    print(
        f"Investment if no extra payment towards SFE: £{investment_if_no_extra_payment:.2f}"
    )

    # scenario 2, pay off SFE ASAP
    years_to_payoff_early = calculate_years_to_payoff_sfe(
        loan_amount,
        interest_rate,
        salary=salary,
        write_off_years=write_off_years,
        optional_extra_payment=disposable_income,
    )
    print(f"Years to payoff SFE if paying extra: {years_to_payoff_early:.2f} years")
    if years_to_payoff_early < write_off_years:
        investment_after_payoff = calculate_investment_growth(
            0,
            annual_return_rate,
            write_off_years - years_to_payoff_early,
            monthly_contribution=disposable_income,
        )
        print(f"Investment after paying off SFE early: £{investment_after_payoff:.2f}")

    # scenario 3, pay off SFE using some disposable income, invest the rest
    disposable_income_split = disposable_income / 2
    years_to_payoff_split = calculate_years_to_payoff_sfe(
        loan_amount,
        interest_rate,
        salary=salary,
        write_off_years=write_off_years,
        optional_extra_payment=disposable_income_split,
    )
    print(f"Years to payoff SFE with split payment: {years_to_payoff_split:.2f} years")

    investment_after_payoff_split = calculate_investment_growth(
        0,
        annual_return_rate,
        write_off_years,
        monthly_contribution=disposable_income_split,
    )
    print(
        f"Investment after paying off SFE early with split: £{investment_after_payoff_split:.2f}"
    )

    # in general this is okay, but people's salaries increase over time, so we should factor that in too
    # for now, let's just assume a fixed salary increase rate


def calculate_sfe_contributions(salary, threshold=27295, rate=0.09):
    if salary <= threshold:
        return 0
    return (salary - threshold) * rate / 12  # monthly contribution


def net_income(salary, tax_rate=0.20, national_insurance_rate=0.12):
    tax = salary * tax_rate
    ni = salary * national_insurance_rate
    return salary - tax - ni


def main():
    salary = 10000000  # annual salary
    loan_amount = 20000  # initial student loan amount
    interest_rate = 5.0  # annual interest rate on the loan
    write_off_years = 30  # years after which the loan is written off
    disposable_income = (
        net_income(salary) / 12 - 2000
    )  # monthly disposable income after expenses
    annual_return_rate = 7.0  # expected annual return rate from investments

    auto_monthly_payment = calculate_sfe_contributions(salary)
    print(f"Auto monthly SFE payment: £{auto_monthly_payment:.2f}")

    compare_strategies(
        salary,
        loan_amount,
        interest_rate,
        auto_monthly_payment,
        write_off_years,
        disposable_income,
        annual_return_rate,
    )


def salary_increase(salary, increase_rate, years):
    return salary * ((1 + increase_rate / 100) ** years)


if __name__ == "__main__":
    main()
