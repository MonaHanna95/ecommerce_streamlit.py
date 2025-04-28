import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#load data

uploaded_file = st.file_uploader("Upload your ecommerce CSV", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

  #convert created_at to datetime
    df['created_at']=pd.to_datetime(df['created_at'],errors='coerce')


    st.title('Pakistan Ecommerce Marketing Dashboard')
    st.markdown('An interacive dashboard to monitor key marketing metrics and sales performance')
    pastel_colors = sns.color_palette('pastel')

    #calculate KPIs
    total_revenue = df['grand_total'].sum()
    total_orders = df['qty_ordered'].sum()
    average_order_value = total_revenue/total_orders

    #display KPIs
    st.metric("Total Revenue",f"${total_revenue:,.2}")
    st.metric("Total Orders",f"${total_orders:,.2}")
    st.metric("Average Order Value",f"${average_order_value:,.2}")


    # Group by 'Month_Year' and sum 'grand_total'
    df['YearMonth'] = df['created_at'].dt.to_period('M')
    monthly_revenue = df.groupby('YearMonth')['grand_total'].sum().reset_index()
    monthly_revenue['YearMonth'] = monthly_revenue['YearMonth'].dt.to_timestamp()

    #plot
    fig,ax = plt.subplots(figsize=(10,5))

    sns.lineplot(data=monthly_revenue,x='YearMonth',y='grand_total',ax=ax)

    st.subheader("Monthly Revenue")
    ax.set_xlabel('Date')
    ax.set_ylabel('Revenue ($)')
    st.pyplot(fig)

    #top selling products
    top_products= df['sku'].value_counts().head(5)
    st.subheader("Top 5 Products")
    fig2, ax2 = plt.subplots()
    sns.barplot(x=top_products.values, y=top_products.index, palette=pastel_colors, ax=ax2)
    ax2.set_xlabel("Units Sold")
    ax2.set_ylabel("SKU")
    st.pyplot(fig2)

    # Best Revenue-Generating Products
    st.subheader("Top Revenue-Generating SKUs")

    top_revenue = df.groupby('sku')['grand_total'].sum().sort_values(ascending=False).head(10)

    fig3, ax3 = plt.subplots()
    sns.barplot(x=top_revenue.values, y=top_revenue.index, palette=pastel_colors, ax=ax3)
    ax3.set_xlabel("Revenue ($)")
    ax3.set_ylabel("SKU")
    st.pyplot(fig3)

    #top selling categories
    top_categories = df['category_name_1'].value_counts().head(5)
    st.subheader("Top 5 Categories")
    fig4, ax4 = plt.subplots()
    sns.barplot(x=top_categories.values, y=top_categories.index, palette=pastel_colors, ax=ax4)
    ax4.set_xlabel("Number of Orders")
    st.pyplot(fig4)

    #revenue by category
    Revenue_by_category = df.groupby('category_name_1')['grand_total'].sum().sort_values(ascending=False).head(10)
    st.subheader("Revenue by Category")
    fig5,ax5 = plt.subplots()
    sns.barplot(y=Revenue_by_category.index, x=Revenue_by_category, palette=pastel_colors, ax=ax5)
    #pastel_colors_hex = [matplotlib.colors.to_hex(color) for color in pastel_colors]
    #st.bar_chart(Revenue_by_category,color=pastel_colors_hex)
    ax5.set_xlabel("Revenue ($)")
    ax5.set_ylabel("Category")
    st.pyplot(fig5)

    #Returning vs new customers
    repeat_customer = df['Customer ID'].value_counts()
    return_customer = (repeat_customer>=2).sum()
    new_customer = (repeat_customer<2 ).sum()
    st.subheader("Customer Insight")
    #st.write(f"Number of returning customers: {return_customer}")
    #st.write(f"Number of new customers: {new_customer}")
    st.metric("Number of returning customers",f"{return_customer}")
    st.metric("Number of new customers",f"{new_customer}")

    #payment method analysis in donut chart 
    payment_summary = df.groupby('payment_method')['grand_total'].sum().sort_values(ascending=False)

    # Keep only top 5 and group the rest into 'Other'
    top5 = payment_summary.head(5)
    others = payment_summary.iloc[5:].sum()
    payment_summary_top5 = pd.concat([top5, pd.Series({'Other': others})])


    # Calculate percentages
    payment_percent = payment_summary_top5 / payment_summary_top5.sum() * 100

    # Plot donut chart
    fig6, ax6 = plt.subplots()
    wedges, texts, autotexts = ax6.pie(
        payment_percent, 
        labels=payment_percent.index, 
        autopct='%1.1f%%', 
        startangle=90,
        counterclock=False,
        colors=pastel_colors,
        wedgeprops={'width': 0.4}
    )
    ax6.axis('equal')
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)

    st.pyplot(fig6)

    #order status
    Status_count=df['status'].value_counts()
    st.subheader("Order Status Distribution")

    # Keep only top 4 and group the rest into 'Other'
    top4_Status = Status_count.head(4)
    others_Status = Status_count.iloc[4:].sum()
    Status_count_top4 = pd.concat([top4_Status, pd.Series({'Other': others_Status})])
    # Calculate percentages
    Status_count_P = Status_count_top4 / Status_count.sum() * 100

    # Plot pie chart
    fig, ax = plt.subplots()
    ax.pie(Status_count_P, labels=Status_count_P.index, autopct='%1.1f%%', startangle=90, counterclock=False, colors=pastel_colors)
    ax.axis('equal')  # Equal aspect ratio to make the pie circular
    st.pyplot(fig)

    #discount impact on sales
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=df, x='discount_amount', y='grand_total', ax=ax)
    st.subheader("Discount Amount vs. Basket total")
    ax.set_xlabel('Discount Amount')
    ax.set_ylabel('Basket total ($)')
    st.pyplot(fig)

else:
  st.warning("Please upload a file to continue.")
