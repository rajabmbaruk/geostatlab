def apply_policy(df, policy, intensity):

    df = df.copy()

    if policy == "Agriculture Boost":
        df["Agricultural_Output"] *= (1 + intensity/100)

    elif policy == "Education Investment":
        df["Education_Level"] *= (1 + intensity/100)

    elif policy == "Employment Program":
        df["Unemployment_Rate"] *= (1 - intensity/100)

    return df