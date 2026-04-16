# Mental-Health-Risk-Profile# Mental Health Risk Profiling using Survey Data

## Overview

Mental health conditions such as depression and anxiety are increasingly prevalent, yet early identification remains a challenge due to limited accessibility and interpretability of screening tools. This project develops a data-driven framework to estimate **relative mental health risk** using large-scale population survey data.

The objective is not to provide clinical diagnosis, but to construct an interpretable system that captures how demographic, behavioral, and psychosocial factors contribute to mental health outcomes.

---

## Project Pipeline

The workflow follows a structured pipeline:

$$
\text{Raw Data} \rightarrow \text{Feature Filtering} \rightarrow \text{Model Training} \rightarrow \text{Validation} \rightarrow \text{Deployment}
$$

A key emphasis of this project is the transition from a high-dimensional dataset to a **carefully curated non-leaky feature space** suitable for real-world deployment.

---

## Dataset and Target Definition

The dataset consists of a large-scale Canadian population survey with over 600 variables capturing demographic, socioeconomic, and mental health indicators.

The primary target variable is:

$$
\text{SCRDDEP} =
\begin{cases}
1 & \text{Screened in (positive)} \\
0 & \text{Screened out (negative)}
\end{cases}
$$

It is important to note that this variable represents a **screening outcome**, not a clinical diagnosis. This distinction guides the interpretation of all model outputs.

---

## Feature Selection and Leakage Prevention

The original dataset contained over 600 variables, many of which were:

- Directly derived from mental health screening instruments  
- Strong proxies for the target variable  
- Highly correlated redundant features  

To prevent leakage, over 400 variables were removed. The final feature set includes only:

- Demographic variables (age, gender, education)  
- Behavioral variables (physical activity)  
- Psychosocial indicators (stress, coping, social support)  
- Functional and interaction measures  

This ensures that the model estimates:

$$
P(Y = 1 \mid X_{\text{realistic}})
$$

rather than relying on hidden or circular signals.

---

## Model Performance

<p align="center">
  <img src="images/roc_curve.png" width="500"/>
</p>

The final model achieves:

- ROC-AUC $\approx 0.75$  
- Accuracy $\approx 0.69$  

Rather than maximizing performance, the model prioritizes **robustness and interpretability**, ensuring that predictions generalize beyond the dataset.

---

## Modeling Approach

Multiple models were evaluated, including:

- Logistic Regression  
- Random Forest  
- XGBoost  

Although XGBoost achieved higher predictive accuracy, the final model selected was a **calibrated logistic regression model**:

$$
P(Y = 1 \mid X) = \frac{1}{1 + e^{-(\beta_0 + \beta^T X)}}
$$

This choice was motivated by:

- Interpretability of coefficients  
- Stability under feature constraints  
- Compatibility with probability calibration  
- Suitability for sensitive domains such as mental health  

---

## Feature Importance and Interpretation

<p align="center">
  <img src="images/feature_importance.png" width="600"/>
</p>

The model identifies several key drivers of depression risk:

- Negative social interaction  
- Functional difficulty  
- Life satisfaction  
- Perceived stress  
- Coping ability  

The sign of coefficients provides directional insight:

- Positive coefficients $\Rightarrow$ increase in risk  
- Negative coefficients $\Rightarrow$ protective effect  

These findings are consistent with established research in mental health and social epidemiology.

---

## Synthetic Profile Validation

<p align="center">
  <img src="images/profile_comparison.png" width="700"/>
</p>

To validate model behavior, synthetic user profiles were constructed to simulate real-world scenarios.

Let $X_1, X_2, ..., X_n$ represent different profiles. The model produces:

$$
P(Y = 1 \mid X_1) \ll P(Y = 1 \mid X_n)
$$

for low-risk vs high-risk individuals.

This confirms that the model captures **meaningful behavioral gradients** rather than producing uniform predictions.

---

## Deployment

The model is deployed as an interactive web application using Streamlit.

Users can input:

- Demographic information  
- Lifestyle indicators  
- Psychosocial conditions  

The application returns:

- Relative Risk Score  
- Risk Classification  
- Psychosocial Radar Profile  
- Model-based explanatory factors  

The predicted probability $\hat{p}$ is transformed into a relative index:

$$
\text{Risk Index} = \frac{\hat{p} - p_{\min}}{p_{\max} - p_{\min}}
$$

to improve interpretability for users.

---

## Ethical Considerations

This project does not provide medical diagnosis or treatment recommendations.

Key limitations include:

- The target variable is a screening measure  
- Predictions are based on population-level trends  
- Individual outcomes cannot be guaranteed  

All outputs should be interpreted as **relative indicators**, not clinical judgments.


## Conclusion

This project demonstrates how careful feature selection, statistical reasoning, and model design can produce an interpretable and deployable machine learning system.

By prioritizing transparency over raw predictive power, the final model provides meaningful insights into mental health risk while remaining aligned with real-world constraints.

The work highlights the importance of designing machine learning systems that are not only accurate, but also responsible, explainable, and practical.
