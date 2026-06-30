import streamlit as st

st.set_page_config(page_title="Education Hub", layout="wide")

from ui_components import apply_custom_sidebar
apply_custom_sidebar()

st.title("🎓 The Education Hub: From 'What is this?' to 'I am a Quant'")

st.markdown("""
So picture this: It's 2 AM, I'm staring at a brokerage app that looks like an Excel spreadsheet from 1998, and my eyes are bleeding. I realized something: Wall Street quants have these insane, multi-million dollar Bloomberg Terminals that visualize market chaos in real time, while the rest of us are stuck looking at 2D line charts that tell us nothing about the actual *vibe* of the market. 

I decided that was unacceptable. So, I set out to build something that takes the most headache-inducing, esoteric math in finance and turns it into a visually stunning, interactive dashboard. I wanted to build an institutional-grade options analytics suite, but make it actually look good.

**How did I pull it off?** 
I basically duct-taped together a bunch of high-octane Python libraries. I'm hitting financial APIs live to rip real-time options chain data straight from the source. Then, I'm throwing that raw data into a blender with `scipy` and `numpy` to run intense Black-Scholes calculations and Newton-Raphson root-finding algorithms (I'll explain what those mean in a second, please don't close the tab). Finally, I wrapped the whole thing in a sleek `Streamlit` frontend and used `Plotly` to render the 3D graphics you can actually spin around with your mouse. 

It’s basically a full-stack quantitative analytics engine, and I built it to look like it belongs in the year 2026.

Now, if you're looking at that 3D surface on the main page and wondering if it's a topographical map of Mars, let's break down the actual math and the markets in plain English. No PhD required.
""")

st.markdown("---")

st.header("1. What Even Is An Option?")
st.markdown("""
Think of an **Option** like a pre-order ticket or a reservation. It gives you the *right*, but absolutely not the obligation, to buy or sell a stock at a locked-in price by a certain date. 

- **Call Option:** The right to **buy**. Imagine you lock in a price to buy the next iPhone at $1,000. If the actual price skyrockets to $1,500 on launch day because of a leak, your ticket is suddenly super valuable because you can still buy it for $1,000 and flip it. (You want the stock to go UP 🚀).
- **Put Option:** The right to **sell**. Imagine you buy insurance to sell your used 2008 Honda Civic for $5k no matter what. If the engine literally blows up tomorrow and it's suddenly worth $500 in scrap, your insurance contract is carrying the team. You still get your 5k. (You want the stock to go DOWN 📉).
- **Strike Price:** The locked-in price we just talked about (the $1,000 iPhone or the $5,000 Civic).
- **Expiration Date:** The day your ticket expires and becomes a literal useless piece of paper (or, well, deleted digital data).
""")

st.header("2. Black-Scholes: The Formula That Broke Wall Street")
st.markdown("""
Back in 1973, some terrifyingly smart math guys (Black, Scholes, and Merton) figured out a formula to actually put a "fair price" on these options. Before this, traders were basically guessing. The Black-Scholes formula says the fair price depends on 5 things:

1. **Current Stock Price** (Where we're at right now)
2. **Strike Price** (Our target locked-in price)
3. **Time left until it expires** (Tick tock)
4. **Risk-Free Interest Rate** (Basically what you'd get leaving cash in a boring savings account)
5. **Volatility (How crazy the stock is swinging)**

Here's the plot twist, and how I built the backend of this app: We *already know* what the option is trading for in the real world on the stock market. We can literally just look at the price. So instead of using the formula to solve for the price, quants (and this app) use the formula in *reverse* to figure out the **Volatility**. 

I reverse-engineer the math using an algorithm called **Newton-Raphson**. It's a calculus trick that guesses the volatility, checks how wrong it is, and rapidly adjusts until it hits the exact right number. We find the hidden variable the market is trying to hide from us.
""")

st.header("3. Implied Volatility (IV): The Market's Anxiety Meter")
st.markdown("""
When my code reverse-engineers that volatility, we get **Implied Volatility (IV)**. 
IV is basically the market pricing in the *vibe*. It's the expected future chaos of the stock, crowd-sourced by millions of traders placing bets with real money.

- **High IV:** Is a massive tech company announcing earnings tomorrow? Did the Fed Chairman just walk up to a podium looking stressed? The market expects huge, violent swings. Options get super expensive because the "insurance premium" goes way up. People are paying top dollar for protection.
- **Low IV:** Just a normal Tuesday for a boring utility company selling electricity in Ohio. Options are dirt cheap because nobody expects the stock to move an inch.
""")

st.header("4. The 3D Surface (Why Does It Look Like That?)")
st.markdown("""
If the market was completely logical and perfectly rational, the IV for every single option on a stock would be exactly the same. It would look like a perfectly flat plane on the graph. 

Spoiler alert: humans are not rational. We are emotional wrecks.

- **The Volatility Smile/Skew:** People are usually way more terrified of a market crash destroying their portfolio than they are excited for a random rally. Because of this fear, they consistently overpay for Put options (downside protection). This bends the flat plane into a curve, known as a "smile" or a "smirk".
- **Time Dynamics:** Options expiring this Friday behave completely differently than options expiring next year. Short-term options are extremely reactive to sudden news, while long-term options are more chill.

In the app, I map the **Strike Price** on the X-axis (left/right) against the **Time to Expiration** on the Y-axis (forward/back), and make the **Implied Volatility** the Z-axis height (up/down). 

The result? The **3D Volatility Surface**. It is a literal 3D heat map of market fear, greed, and future expectations. When you spin it around, you are looking at the collective psychology of Wall Street rendered in math.
""")

st.header('5. The "Greeks" (Your Dashboard Stats)')
st.markdown("""
The "Greeks" are basically your HUD (heads-up display) in a video game. They tell you exactly how your option's stats will react when the market environment shifts. My app calculates these for every single option on the chain so you aren't flying blind.

### 𝚫 Delta (The Speedometer)
- **What it is:** How much your option's price changes if the stock moves exactly $1.
- **Vibe Check:** If Delta is 0.50, and the stock goes up a buck, your option goes up 50 cents. It's also a Wall Street cheat code for probability—a 0.20 Delta loosely means the market thinks there's a 20% chance the option actually pays out at expiration.

### 𝚪 Gamma (The Accelerator)
- **What it is:** How fast your Delta changes. 
- **Vibe Check:** If Delta is your speed, Gamma is stomping on the gas pedal. It is absolutely highest when the stock price is hovering right around your Strike Price. It means your option's value is extremely sensitive, balanced on a knife's edge, ready to snap violently in either direction.

### 𝚯 Theta (The Bleed)
- **What it is:** How much money your option loses every single day just because time passed.
- **Vibe Check:** Options are basically ice cubes melting in the sun. The closer you get to expiration, the faster they melt. Theta is almost always negative unless you're the one selling (shorting) the option. You are literally paying for time.

### 𝛎 Vega (The Hype Factor)
- **What it is:** How much your option price changes if Implied Volatility jumps by 1%.
- **Vibe Check:** Imagine the stock doesn't move a single inch, but suddenly everyone on Twitter starts panicking and IV spikes. Vega is the stat that makes your option randomly skyrocket in value just because the *vibes* got more chaotic. 

### 𝛒 Rho (The Macro Factor)
- **What it is:** Sensitivity to interest rates changing.
- **Vibe Check:** Honestly? Unless you're buying options that expire in like 3 years, you can mostly ignore this one. It's for the macro nerds obsessing over the Federal Reserve.
""")

st.markdown("---")
st.success("You survived the deep dive. Now hit the main app in the sidebar and start flipping between IV, Delta, and Gamma on the 3D surface to see this stuff in action!")
