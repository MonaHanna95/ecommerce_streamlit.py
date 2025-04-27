import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components

#load data
df = pd.read_csv('cleaned_ecommerce_data.csv',low_memory=False)

#convert created_at to datetime
df['created_at']=pd.to_datetime(df['created_at'],error='ecoerce')


st.title('Pakistan Ecommerce MArketing Dashboard')
st.markdown('An interacive dashboard to monitor key marketing metrics and sales performance')

#calculate KPIs
total_revenue = df['grand_total'].sum()
total_orders = df['qty_ordered'].sum()
average_order_value = total_revenue/total_orders

#display KPIs
st.metric("Total Revenue",f"${total_revenue:,.2f}")
st.metric("Total Orders",f"${total_orders:,.2}")
st.metric("Average Order Value",f"${average_order_value,.2}")

#monthly revenue
monthly_revenue = df.groupby('Month')['grand_total'].sum().reset_index()

#plot
fig,ax = plt.subplot(figsize=(10,5))
sns.lineplot(data=monthly_revenue,x='Month',y='grand_total',ax=ax)
ax.set_title('Month Revenue')
ax.set_xlabel('Month')
ax.set_ylabel('Revenue')
st.pyplot(fig)

#top selling products
top_products= df['sku'].value_counts().head(5)
st.subheader("Top 5 Products")
st.bar_chart(top_products)

#top selling categories
top_categories = df['category_name_1'].value_counts().head(5)
st.subheader("Top 5 Categories")
st.bar_chart(top_categories)

#revenue by category
Revenue_by_category = df.groupby('category_name_1')['grand_total'].sum().sort_values(ascending=False)
st.subheader("Revenue by Category")
st.bar_chart(Revenue_by_category)

#Returning vs new customers
repeat_customer = df['Customer ID'].value_counts()
return_customer = (repeat_customer>1).sum()
new_customer = (repeat_customer<1).sum()
st.subheader("Customer Insight")
st.write(f"Number of returning customers: {return_customer}")
st.write(f"Number of new customers: {new_customer}")

#payment method analysis in donut chart 
payment_summary = df.groupby('payment_method')['grand_total'].sum().sort_values(ascending=False)
payment_percent = payment_summary/payment_summary.sum()*100
colors=sns.color_palette('pastel')[0:len(payment_summary)]
st.subheader("Ravenue by Payment Method")
fig,ax=plt.subplots()
wedges,texts,autotexts = ax.pie(
  payment_percent,
 labels=payment_percent.index,
 autopct='%1.1f%%',
 startangle=90,
 counterclock=False,
colors=colors,
wedgeprops={'width:0.4'}
)

ax.axis('equal')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(10)

st.pyplot(fig)

#order status
Status_count=df['status'].value_counts()
st.subheader("Order Status Distribution")
# Calculate percentages
Status_count = Status_count / Status_count.sum() * 100

# Plot pie chart
fig, ax = plt.subplots()
ax.pie(Status_count, labels=Status_count.index, autopct='%1.1f%%', startangle=90, counterclock=False)
ax.axis('equal')  # Equal aspect ratio to make the pie circular
st.pyplot(fig)

#discount impact on sales
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=df, x='discount_amount', y='grand_total', ax=ax)
ax.set_title('Discount Amount vs. Grand Total')
ax.set_xlabel('Discount Amount')
ax.set_ylabel('Grand Total')
st.pyplot(fig)

# Embed Tableau dashboard
tableau_url = "https://public.tableau.com/views/Dashboardecommerce_17455112809460/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
components.iframe(tableau_url, width=800, height=600)            

