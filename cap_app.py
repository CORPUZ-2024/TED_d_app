import streamlit as st

import pandas as pd


import plotly.graph_objects as go

import plotly.express as px

from PIL import Image

import os


st.title('Effects of Medicaid  Expansion to Treatment Completions in SUD Outpatient Programs')
##Text below as Preview 
"""
As of January 2014, adults with incomes up to 138% of the Federal Poverty Level ($17,774 for an individual in 2021) became eligible 
for Medicaid benefits under the Affordable Care Act’s (ACA) Medicaid expansion program. All but 12 states have adopted
 the Medicaid expansion decision in their state.
"""


st.header('Overview')
"""
In investigating the causal relationship between Medicaid expansion and successful treatment completions for substance use disorder, 
the Difference -in- Differences Model and Two-way Fixed Effects model were used to analyze a panel data of discharge events between 2009 and 2019. 
"""

st.header('Dataset')

"""
TEDS-D dataset tracks the annual discharges (TEDS-D) from substance use treatment facilities. Publications between 2009 and 2019 were converged
to create a master dataset containing 17 million entries and 62 features. This initial dataset was subsetted to only contain outpatient treatment 
episodes which reduced the working dataframe to  around 7 million entries and 39 columns. The preprocessing methods are discussed in detail in this Jupyter Notebook.

**Excluded Data** Five states were dropped due to inconsistent data submissions between 2009 and 2019. 
These states were West Virginia, Oregon, Georgia, South Carolina and Washington.

**Retained Features**  The final data frame consisted of both original features and some derived variables. The numeric encodings for
 the original features used “-9” as code for missing values. 

-  **'CASEID':** unique case identifier 
-  **'STFIPS':** Numeric encoding for each State. State names were derived in 'STATE_NAME' for EDA
- **'DISYR':** Discharge year 
- **'AGE':** Numeric encoding for a certain age range. This variable  was encoded as general categorical age groups in the variable 'AGE_GRP' for EDA. 
- **'GENDER':** Takes the value of 1 for Male, 2 for Female and -9  for missing values. Categorical equivalents are provided in 'Gender_Type' for EDA
- **'RACE':** Numeric encoding for each race category.  This variable  was encoded as general categorical values in   'Race_Categ’ for EDA. 
- **'EDUC':**  Numeric encoding for education level where high positive value indicates higher education level. 
- **'EMPLOY':** Numeric encoding for employment status at admission where the least positive value (1) indicate full employment
- **'DETNLF':** Numeric encoding for detailed not in-labor force category. 
- **'PREG**': Takes the value of 1 for pregnant subjects, 2 otherwise. 
- **'VET':**  Takes the value of 1 for veteran subjects, 2 otherwise. 
- **'LIVARAG'** : Numeric encoding for living arrangements during admission where a value of 1 means Homeless. Binary and 
       categorical equivalents were derived in 'Homeless' for EDA
- **'PRIMINC':** Numeric encoding for source of income/support
- **'SERVICES_D':** Numeric encoding for service type (outpatient, inpatient et) 
- **'METHUSE':** Value of 1 indicates the use of Medication-assisted opioid therapy and 2 otherwise 
- **'REASON':** Numeric encoding for Reason for discharge. Binary and categorical values were derived in ‘reason_coded’ where the 
       value of 1 indicates successful treatment completions and 0 otherwise.  
- **'LOS':** Numeric encoding for length of stay in treatment (in terms days)
- **'NOPRIOR':** Binary encoding for previous substance use treatment episodes where a value of 1  indicates one or more prior treatment episodes and 0 otherwise. 
- **'DSMCRIT':** Numeric encoding for primary diagnosis 
- **'PSYPROB':** Value is 1 for  co-occurring mental and substance use disorders and 0 otherwise 
- **'PRIMPAY':** Numeric encoding for primary payment source. Binary and categorical equivalent derived in  'Payment_Type' where 1 indicates the use  of Medicaid and 0 otherwise. 
- **'Treat':** dummy variable that is equal to 1 for states that adopted the expansion  for a given year
- **'Imp_Year':** The year when a state implemented the Medicaid expansion 
- **'Post':** dummy variable that is equal to 1 for years post expansion (2014 onwards)
- **'DID':** Interaction variable interaction variable which will represent the states that

"""


####### Data Uploads
## For Regression 
#outp_7m_3= pd.read_csv('C:/Users/16502/Documents/Capstone/outp_7m_3a.csv')


## Shows first n entries of the df 
#st.write(outp_7m_3.head(6))

st.header('Exploratory Data Analysis')
"""
In this section, we explore some of the features to get more insights on the treatment outcomes and demographic information of the
 individuals represented in this dataset which we refer to as PiRs (Persons in Recovery) in this section . 

**Discharge Rates:** Overall, the median annual discharge rates nationwide remained between 40% to 30 %  with the highest median level recorded 
in 2009 at 43.5% which steadily declined in the following years. Furthermore, the spread for each year tended to be normal in distribution among the states. 

"""




dis_rate= pd.read_csv("./main/dis_rate_agg.csv")

fig_dis2 = px.box(dis_rate, x="year", y="tmp_rate",notched=True,  hover_data=["state"], color_discrete_sequence=[ "#e884d6"])
fig_dis2.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
fig_dis2.update_layout(title_text= "<b>Discharge Rate Between 2009 - 2019</b>", title_x=0.5)
fig_dis2.update_xaxes(nticks=15) 

st.plotly_chart(fig_dis2)



"""
**Medicaid as Primary Payment Source:** Since our analysis is focused on the effects of Medicaid on treatment outcomes, it might be relevant to know the 
rate of which Medicaid was used as the primary payment source at admission. While the mean rate stayed between 0% to 20% ,
there is a noticeable positive skew in the distribution for each year meaning that there are many states that recorded
Medicaid utilization rates that are higher than the average. The degree of the positive skew peaked in 2009 at 52% then 
decreased to around 35% to 28% in the following years until 2013. A similar pattern occurred between 2013 and 2019. 
"""
ptype_rate= pd.read_csv("C:/Users/16502/Documents/Capstone/ptype_rate.csv")

fig_ptype = px.box(ptype_rate, x="year", y="medicaid_use",notched=True, hover_data=["state"],  color_discrete_sequence=[ "#01661e"])
fig_ptype.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
fig_ptype.update_layout(title_text= "<b>Medicaid as Primary Payment Souce </b>", title_x=0.5)
fig_ptype.update_xaxes(nticks=15) 

st.plotly_chart(fig_ptype)

"""
**Prior Treatment Attendance:** In terms of the percentage of treatment episodes that involved someone that had previous treatments before, the distribution 
tended to be normal with a median rate fluctuating between 48% and 52% from 2009 to 2014. However the spread between 2015 and 2018 became concentrated between 30% to 60% as indicated by the shorter whiskers but the median rates stayed in the 49 % plus range. This change indicates that more states reported treatment 
episodes that involved individuals with prior treatment history between 2015-2018. However, an almost normal spread with a slight positive skew was recorded
for 2019 with the median rate of 39% which only means that while a lot more of the states reported rates in the 40s and above,there were also states 
with lower percentage of folks with prior treatment episodes which was not the case in the previous 4 years.  
"""
prior_rate= pd.read_csv('C:/Users/16502/Documents/Capstone/prior_rate.csv') 
fig_prior = px.box(prior_rate, x="year", y="discharge_rate",notched=True, hover_data=["state"], color_discrete_sequence=[ "#b83209"])
fig_prior.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
fig_prior.update_layout(title_text= "<b> Prior Treatment Attendance </b>", title_x=0.5)
fig_prior.update_xaxes(nticks=15) 

st.plotly_chart(fig_prior)

"""
**Homelessness among Persons in Recovery:** Overall, homelessness seems to be a minor issue among the individuals in this dataset given that the 
median percentage of homeless PiRs across the states hovered below 5% every year. While the range for each year’s spread oscillated throughout the years,
the positive skew of these spreads steadily grew from 2015 onwards which indicated growing prevalence of homelessness among PiRs.  
"""

homeless_rate= pd.read_csv("C:/Users/16502/Documents/Capstone/homeless_rate.csv")
fig_hom = px.box(homeless_rate, x="year", y="homeless_rate",notched=True, hover_data=["state"], color_discrete_sequence=[ "#FF7F0E"] )
fig_hom.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
fig_hom.update_layout(title_text= "<b>Homeless Rate per Year during Admission</b>", title_x=0.5)
fig_hom.update_xaxes(nticks=15) 

st.plotly_chart(fig_hom)

"""
**Age:** About 40% of PiRs in this dataset were between 21 and 34 years old. Individuals between 35 to 49 years old trailed behind at 32%.
"""
labels= outp_7m_3.AGE_GRP.unique().tolist()
values=  [685724, 2449142, 3072901, 1452794]

colors = ['blue','red','lightblue','orange']
fig_age = go.Figure(data = go.Pie(values = values, 
                          labels = labels, hole = 0.4,
                          title = "<b> Age Distribution </b>",
                          marker_colors = colors
                 ))
st.plotly_chart(fig_age)
"""
**Race:** White PiRs significantly outnumbered all of the other race categories each year with African Americans being the second largest group. 
"""
race_agg = pd.read_csv('C:/Users/16502/Documents/Capstone/race_agg2.csv')
fig_race = px.histogram(race_agg, 
            x="DISYR", 
            y="count", 
            barmode="group",
            color="Race_Categ", 
            title="<b> Race Categories Among PiRs </b>")
fig_race.update_xaxes(type="category")
fig_race.update_layout(yaxis_title="Count")
st.plotly_chart(fig_race)

"""
**Gender:** Men significantly outnumbered women in this dataset.  
"""
gender_agg = pd.read_csv('C:/Users/16502/Documents/Capstone/gender_agg.csv')
fig_gender = px.histogram(gender_agg, 
            x="DISYR", 
            y="count", 
            barmode="stack",
            color="Gender_Type", 
            title=" <b>Gender Distribution Among PiRs </b>")
fig_gender.update_xaxes(type="category")
fig_gender.update_layout(yaxis_title="Count")

st.plotly_chart(fig_gender)


st.header('Trade Offs with Data')
"""
The dataset with over 7 million entries is able to produce more insights in terms of the trends and distribution of some features of interest.
However, the dataset coded missing values as -9 which will impact  the regression results. The most conservative approach was used in this case 
and entries with -9 encodings were removed. This dramatically reduced the dataset to over 1 million entries. 

In examining how the distribution of states based on the implementation year changed between the 7 million set and the 1 million set, the following 
graphics were generated. In the full dataset, it can be observed that the states that eventually implemneted the expansion in 2014 were more represented 
in the pre and post-treatment periods compared to the other groups. While the the "Never" group followed the seasonal pattern of the 2014 implementers
but in lower volumes, the 2015 group steadily increased over time. Lastly, the 2016 group remained relatively constant. 

"""

imp_yr_agg=  pd.read_csv('C:/Users/16502/Documents/Capstone/eda_sets/imp_yr_agg.csv')

fig_s = px.histogram(imp_yr_agg, 
            x="DISYR", 
            y="count", 
            barmode="group",
            color="Imp_Year", 
            title="<b> Entries by Implementation Year for the 7M Set </b>")
fig_s.update_xaxes(type="category")
fig_s.update_layout(yaxis_title="Count", width= 700, height= 700)
st.plotly_chart(fig_s)

"""
In contrast, the 1 million set has more of a staggered pattern as opposed to the wave like patterb from the earlier plot. Also, the 2016 implementers
seemed to gradually decrease in numbers as opposed to being constant. The likeness between the 1m and 7m sets may not be that consistent but 
the overall seasonality and level of representation of the treatment and the control states are still reminiscent of the 7m set. Therefore, we can 
proceed with some caution in using the 1m set in our regressions. 
"""
imp_yr_agg_1m= pd.read_csv('C:/Users/16502/Documents/Capstone/eda_sets/imp_yr_agg_1m.csv')
fig_sm = px.histogram(imp_yr_agg_1m, 
            x="DISYR", 
            y="count", 
            barmode="group",
            color="Imp_Year", 
            title="<b> Entries by Implementation Year for the 1M Set </b>")
fig_sm.update_xaxes(type="category")
fig_sm.update_layout(yaxis_title="Count", width= 700, height= 700)
st.plotly_chart(fig_sm)

st.header('Methodology')

"""
Difference -in- Differences Model (DiD) estimates the treatment effects of an intervention (like a policy change like the Medicaid Expansion) by comparing the
differences in observed outcomes between treatment and control groups, across pre-treatment and post-treatment periods. In this analysis, the treatment 
group would be the states that adopted the expansion while the control group would be the states that deferred from implementing the expansion. 
Also, the pre-treatment period are the years between 2009 and 2013 while the post-treatment period are the years from 2014 to 2019. 

**The functional form for this model is pictured below.**
"""
st.latex(r'''
^{}Y_{discharge_status} = \beta_{0} + \beta_{1}Treat + \beta_{2}Post + \beta_{3}(Treat*Post)+ \beta_{4}Other Covariates + v_{ij} + u
'''
)

st.latex(r'''
\newline\beta_{0} = The\ mean\ value\ of\ the\ response\ variable\ when\ all\ of\ the\ predictor\ variables\ in\ the\ model\ are\ equal\ to\ zero
\newline \beta_{1}Treat = Dummy\ variable\ that\ is\ equal\ to\ 1\ for\ states\ that\ adopted\ the\ expansion
\newline \beta_{2}Post = Dummy\ variable\ that\ is\ equal\ to\ 1\ for\ the\ years\ during\ the\ treatment\ period\ (2014\ and\ onwards)
\newline \beta_{3}(Treat*Post)= Interaction\ variable\ that\ represent\ the\ states \newline
                             that\ implemented\ the\ expansion\ during\ the\ treatment\ period 
'''
) 

"""
The validity of the results of our DiD model is dependent on proving the Parallel Trend assumption. This assumption uses the control group as a 
proxy for the counterfactual trend. Specifically, if both the treatment and control groups had parallel trends for a certain outcome and 
a drastic deviation from the treatment group occurs during the treatment period, then this change can be attributed to the differential effect of the intervention. 

To illustrate the Parallel Trend Assumption, the mean discharge status value for treatment and control states were plotted against discharge year with the 
treatment states grouped according to its respective implementation year to account for the staggered adoption of the expansion. 
"""
dd_pta = Image.open("C:/Users/16502/Documents/Capstone/paral_outp.jpg")
st.image(dd_pta)


"""
The resulting graph shows no clear parallel trend among the states pre-intervention period and thus we cannot confidently say that a counterfactual scenario 
is modeled by the control group which is an essential aspect of the DiD estimation. Given that we are comparing states of various sizes and different
ideologies/cultures in terms of how substance use disorder is treated, it makes intuitive sense that proving the Parallel Trend assumption would be challenging. 
While no immediate effect on average discharge status can be observed after 2014, a noticeable increase can be seen for the 2014 implementers around 2017
onwards while the opposite is true for the 2016 group where a dip can be observed after 2016. 
"""
#dis_rate_imp= pd.read_csv('C:/Users/16502/Documents/Capstone/dis_rate_imp.csv')
dd_pta_disrate = Image.open("C:/Users/16502/Documents/Capstone/para_dis_rate.jpg")
st.image(dd_pta_disrate)

"""
Since the 1 million set would be used for the regressions, an analogous plot was generated using this dataset. The lines for each group are smoother 
compared to the 7m set which means that we do lose a lot of context by using the 1m set. More importantly, the significant increase and decrease 
in average discharge status for the 2014 and 2016 implementers respectively was not evident in the 1m set.


Overall, the Medicaid expansion might not be as impactful - if not potentially mildly detrimental- to treatment outcomes based on these preliminary plots. 
"""


st.subheader('Two-way Fixed Effects Model')
"""
If the Parallel Trend Assumption cannot be observed clearly, then there must be unobserved factors that are correlated with both treatment status and timing of the treatment.
These unobserved heterogeneity or time invariant yet subject specific variation across the states and PiRs are factors that the Fixed-Effects Model accounts
for by assuming that the  independent variables are constant.  Therefore, only the dependent variable changes in response to independent variables. 

Since, the Parallel Trend Assumption cannot be clearly demonstrated in this dataset, the Two Way Fixed Effects was used as a secondary model. 

**The functional form for this model is pictured below.**
"""

st.latex(r'''
y_{it} = \alpha + \beta * Treat_{it} + \gamma_t + \delta_i + \lambda_{it} + \epsilon_{it} \newline
y_{it} = Treatment\ outome\ for\ a\ given\ state\ in\ a\ given\ year \newline
\alpha = The\ mean\ value\ of\ the\ response\ variable\ \newline
when\ all\ of\ the\ predictor\ variables\ in\ the\ model\ are\ equal\ to\ zero \newline
\beta * Treat_{it} = Implementation\ status\ for\ a\ given\ state\ in\ a\ given\ year \newline
\gamma_t = Time\ invarient\ variables\ eg. sex, race \newline
\delta_i= entity\ effects\ \newline
\lambda_{it}= Other\ covariates\ for\ each\ state \newline
\epsilon_{it} = error\ term 

'''
)
st.header('Models and Results')

"""
While we know that the Parallel Trend Assumption was not fulfilled in this case, it might still be interesting to compare the DID model with the FE models. 
Also, a comparative model for each type was also generated without the “RACE” variable to check for robustness.
<p> 
**How to Analyze the Results:** Again, the F Statistic Score was assessed  in addition to the respective p values of each coefficient.  The ideal value 
for F Statistic >10 while we want small p values.  
"""

dd_v = """
dd_v= ols(formula='reason_coded ~  Treat + Post + DID + AGE + GEN + VET + RACE +EMPLOY + EDUC + homeless + MAT + PRIOR + SUB1 + PRIMPAY+ PSY', data=outp_ols).fit()
dd_v.summary()
"""
st.code(dd_v, language='python')

dd_rt = """
dd_rt= ols(formula='reason_coded ~  Treat + Post + DID + AGE + GEN + VET +EMPLOY + EDUC + homeless + MAT + PRIOR + SUB1 + PRIMPAY+ PSY', data=outp_ols).fit()
dd_rt.summary()
"""
st.code(dd_rt, language='python')

##results dd
dd_res = Image.open("C:/Users/16502/Documents/Capstone/dd_modsf.jpg")
st.image(dd_res)

"""
**Analysis of DiD Models:** 
In comparing the F Statistic scores between the 2 DiD Models, the model without the "RACE" variable had a marginally larger F Statistic score but both models had F Stats > 10.  
The p values of the coefficients in both models were also statistically significant which means that there is less than 1% chance that these variables are not significant. 
 
The **DID** variable had a coefficient of -0.037*** which means that being an adopter of medicaid expansion translated to -.037 less points towards a successful treatment completion. 
Given that intercept is 0.574*** the DID's effect is very small but negative and statistically significant nonetheless. Despite of this, we were unable to conclude anything about 
the differential effect of the medicaid expansion to treatment outcomes since the Parallel Trend assumption was not proven initially.
 
In terms of the other covariates, age, education, being a man, race and being a veteran were positively correlated with treatment completions. However,  
being employed, participating in Medication Assisted Therapy, payment type used, having prior treatment episodes, having psychological comorbidities, 
being homeless and the type of substance being abused were all negatively correlated with treatment completions.
"""

st.header('Two-Way Fixed Effects')

FE_v = """
FE_v = ols(formula='reason_coded ~  Treat +C(DISYR) + C(STFIPS) + AGE + GENDER + VET + RACE +EMPLOY + EDUC + LIVARAG + METHUSE + NOPRIOR + SUB1 + PRIMPAY + PSYPROB ', data = outp_ols).fit()
FE_v.summary()
"""
st.code(FE_v, language='python')


FE_rt = """
FE_rt = ols(formula='reason_coded ~  Treat +C(DISYR) + C(STFIPS) + AGE + GENDER + VET +EMPLOY + EDUC + LIVARAG + METHUSE + NOPRIOR + SUB1 + PRIMPAY + PSYPROB ', data = outp_ols).fit()
FE_rt.summary()
"""
st.code(FE_rt, language='python')

##results 2W
fe_res = Image.open("C:/Users/16502/Documents/Capstone/fe_modsf.jpg")
st.image(fe_res)

"""
**Analysis of FE Models:** 
In comparing the F Statistic scores between the 2 FE Models, the model without the "RACE" variable had a marginally larger F Statistic score but both models again had 
F stats that were > 10. The p values of the coefficients in both models were also statistically significant which means that there is less than 1% chance that these 
variables are not significant. 
    
The **Treat** variable had a coefficient of 0.014*** which means that being an adopter of medicaid expansion translated to  **.014 more points towards 
a successful treatment completion**. This is in contrast to the DiD Model that estimated a negative and partially larger coefficient compared to the FE Models. 

    
Furthermore, while both models had positive intercepts, the FE models had a coefficient of 0.468*** which was smaller than the  DID's estimated effect.

In terms of the other covariates, age, education, being a man, race and being a veteran were positively correlated with treatment completions. However,  being employed, 
participating in Medication Assisted Therapy, payment type used, having prior treatment episodes, having psychological comorbidities, being homeless and the 
type of substance being abused were all negatively correlated with treatment completions.Still, the MAT coefficient had the largest degree of effect 
at -0.220***which was similar to the DiD's estimation. 
"""

st.header('Analysis')
"""
Based on the model specifications of FE models in regards to panel data like the TEDs-D dataset, it might be possible that the FE model is the more accurate model of the two. 
However, in plotting the mean discharge rates across the years based on the implementation type, we know that the overall trend for the 2014 implementers was downward sloping 
which is in contrast to the FE estimator for the FE model. 

To further analyze this discrepancy, an alternative  implementation of the Two-way Fixed Effects model was used. Specifically, the standard errors were clustered. 
By not clustering the standard errors for panel data, the resulting model might be prone to higher estimates for t-statistics , lower p values and narrow confidence 
intervals. Hence, the very small p values for the DiD and Treat coefficients might be due to the unclustered standard errors. 
"""

st.subheader('Alternative Implementation of FE Model')
FE= """
w1=outp_ols.set_index(["STFIPS", "DISYR"])
FE = PanelOLS(w1.reason_coded, w1[['Treat', 'AGE', 'GEN', 'VET', 'RACE', 'EMPLOY', 'EDUC', 'homeless', 'MAT', 'PRIOR', 'SUB1', 'PRIMPAY', 'PSY']],
              entity_effects = True,
              time_effects=True
              )

result = FE.fit(cov_type = 'clustered',
             cluster_entity=True,
             cluster_time=True
             )

#display(result.summary)
"""


st.code(FE, language='python')
"""
The coefficients of the new FE model have the same values as the previous FE Models and only the p values changed for the coefficients. TREAT and PRIMPAY were not significant 
while GEN (or being a man ) was only significant at 95% confidence level. Furthemore, the variable RACE was only significant at 90% CI. The rest of the coefficients 
remained significant at 99% CI. 
"""

st.header('Discussion')

"""
Overall, the positive direction of the ‘Treat’ variable might be due to the unclustered standard errors. In clustering the errors, the estimator remained  positive but the 
p value indicated that it was not statistically significant and therefore, Medicaid expansion did not have a significant effect on treatment completions. This is more 
intuitive than our previous findings from the non-clustered standard error results of the initial FE models given what we know from the plots for the Parallel Trend Assumption. 

Also given that we mainly analyzed the FE models, the results are only generalizable to the states included in the 1m set which included outlier states
like New York and California. Hence, in approaching this inquiry again, other sampling methods and econometric models should be considered to minimize the 
loss of data from significant states and to properly account for all factors that play. 
"""

st.header('Implication')
"""
While the expansion did not have any effect on treatment completions, we did observe that MAT participation was significantly and negatively correlated with treatment completions 
across all the models. Given the range of the intercepts, the -.22 estimator for MAT is pretty large as well. This is an interesting observation given that MAT is touted as
a modality that increases treatment retention  and thus perhaps conducive to successful treatment completions. 

While this project was not able to illuminate the full extent of how medicaid expansion truly affected treatment completions, we did find some indication that states 
might benefit more from MAT through continuous evaluation of its costs and potential health benfits. 
"""

