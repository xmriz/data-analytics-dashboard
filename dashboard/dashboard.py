import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as mpimg
import streamlit as st
from babel.numbers import format_currency

sns.set_theme(style="whitegrid")

# UI configurations
st.set_page_config(page_title="Olist E-commerce Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

# markdown
st.markdown(
    '''
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&random=false&width=435&lines=Olist+E-Commerce;Data+Analysis%3A;By+Ahmad+Rizki)](https://git.io/typing-svg)
'''
)

st.markdown("# :rainbow[Olist E-Commerce Dashboard]")

# Data Overview
st.header('Data Overview')
st.write('''
Olist adalah platform e-commerce terbesar di Brazil yang menyediakan berbagai macam produk.
''')

# Load Data
customer_geolocation_df = pd.read_csv('./data/customer_geolocation.csv')
seller_geolocation_df = pd.read_csv('./data/sellers_geolocation.csv')
order_orderItem_orderPayment_df = pd.read_csv(
    './data/order_orderItem_orderPayment.csv')
product_orderItems_category_df = pd.read_csv(
    './data/product_orderItems_category.csv')
product_orderItems_category_order_df = pd.read_csv(
    './data/product_orderItems_category_order.csv')
order_orderPayment_df = pd.read_csv('./data/order_orderPayment.csv')
order_reviews_df = pd.read_csv('./data/order_reviews.csv')

datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
                 'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in datetime_cols:
    order_orderItem_orderPayment_df[col] = pd.to_datetime(
        order_orderItem_orderPayment_df[col])
    order_orderPayment_df[col] = pd.to_datetime(order_orderPayment_df[col])

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        # Statistik Produk
        st.header('Statistik Produk')

        tab1, tab2 = st.tabs(['Penjualan', 'Pembelian'])

        with tab1:
            st.subheader('Penjualan')

            total_penjualan_per_category_df = product_orderItems_category_df.groupby(
                by='product_category_name_english').size().sort_values(ascending=False).reset_index(name='total_penjualan')
            total_penjualan_per_category_df.rename(
                columns={'product_category_name_english': 'product_category'},
                inplace=True
            )
            st.write(
                f"Total Penjualan: {total_penjualan_per_category_df['total_penjualan'].sum()}")
            st.dataframe(total_penjualan_per_category_df)

            fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 8))
            colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
            sns.barplot(x="total_penjualan", y="product_category", data=total_penjualan_per_category_df.head(
                5), hue="product_category", palette=colors, dodge=False, ax=ax[0])
            ax[0].set_title(
                'Kategori Produk dengan Penjualan Terbanyak', fontsize=16)
            ax[0].set_ylabel(None)
            ax[0].set_xlabel(None)
            ax[0].tick_params(axis='x', labelsize=12)
            for tick in ax[0].get_yticklabels():
                tick.set_rotation(45)

            sns.barplot(x="total_penjualan", y="product_category", data=total_penjualan_per_category_df.tail(
                5).sort_values(by='total_penjualan'), hue="product_category", palette=colors, dodge=False, ax=ax[1])
            ax[1].set_title(
                'Kategori Produk dengan Penjualan Tersedikit', fontsize=16)
            ax[1].set_ylabel(None)
            ax[1].set_xlabel(None)
            ax[1].tick_params(axis='x', labelsize=12)
            for tick in ax[1].get_yticklabels():
                tick.set_rotation(45)

            plt.suptitle('Product Category Sales', fontsize=20)
            plt.legend([], frameon=False)
            st.pyplot()

        with tab2:
            st.subheader('Pembelian')
            total_pembelian_per_category_df = product_orderItems_category_order_df.groupby(
                by='product_category_name_english').size().sort_values(ascending=False).reset_index(name='total_pembelian')
            total_pembelian_per_category_df.rename(
                columns={'product_category_name_english': 'product_category'},
                inplace=True
            )
            st.write(
                f"Total Pembelian: {total_pembelian_per_category_df['total_pembelian'].sum()}")
            st.dataframe(total_pembelian_per_category_df)

            fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 8))
            colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
            sns.barplot(x="total_pembelian", y="product_category", data=total_pembelian_per_category_df.head(
                5), hue="product_category", palette=colors, dodge=False, ax=ax[0])
            ax[0].set_title(
                'Kategori Produk dengan Pembelian Terbanyak', fontsize=16)
            ax[0].set_ylabel(None)
            ax[0].set_xlabel(None)
            ax[0].tick_params(axis='x', labelsize=12)
            for tick in ax[0].get_yticklabels():
                tick.set_rotation(45)

            sns.barplot(x="total_pembelian", y="product_category", data=total_pembelian_per_category_df.tail(
                5).sort_values(by='total_pembelian'), hue="product_category", palette=colors, dodge=False, ax=ax[1])
            ax[1].set_title(
                'Kategori Produk dengan Pembelian Tersedikit', fontsize=16)
            ax[1].set_ylabel(None)
            ax[1].set_xlabel(None)
            ax[1].tick_params(axis='x', labelsize=12)
            for tick in ax[1].get_yticklabels():
                tick.set_rotation(45)

            plt.suptitle('Product Category Purchases', fontsize=20)
            plt.legend([], frameon=False)
            st.pyplot()

    with st.container(border=True):
        # RFM Analysis
        st.header('RFM Analysis')
        recent_date = order_orderPayment_df['order_purchase_timestamp'].max()
        rfm_df = order_orderPayment_df.groupby(by='customer_id', as_index=False).agg({
            'order_purchase_timestamp': lambda x: (recent_date - x.max()).days,
            'order_id': 'nunique',
            'payment_value': 'sum'
        })

        rfm_df.rename(columns={
            'order_purchase_timestamp': 'recency',
            'order_id': 'frequency',
            'payment_value': 'monetary'
        }, inplace=True)

        st.write('RFM Data')
        st.dataframe(rfm_df)

        fig, ax = plt.subplots(3, 1, figsize=(20, 20))

        colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

        sns.barplot(orient='h', data=rfm_df.sort_values(by='recency', ascending=True).head(
            5), x='recency', y='customer_id', hue='customer_id', palette=colors, dodge=False, ax=ax[0])
        ax[0].set_title('Top 5 Customers by Recency', fontsize=15)
        ax[0].set_xlabel('Recency (Days)', fontsize=12)
        ax[0].set_ylabel(None)

        sns.barplot(orient='h', data=rfm_df.sort_values(by='frequency', ascending=False).head(
            5), x='frequency', y='customer_id', hue='customer_id', palette=colors, dodge=False, ax=ax[1])
        ax[1].set_title('Top 5 Customers by Frequency', fontsize=15)
        ax[1].set_xlabel('Frequency', fontsize=12)
        ax[1].set_ylabel(None)

        sns.barplot(orient='h', data=rfm_df.sort_values(by='monetary', ascending=False).head(
            5), x='monetary', y='customer_id', hue='customer_id', palette=colors, dodge=False, ax=ax[2])
        ax[2].set_title('Top 5 Customers by Monetary', fontsize=15)
        ax[2].set_xlabel('Monetary (R$)', fontsize=12)
        ax[2].set_ylabel(None)

        plt.suptitle('RFM Analysis', fontsize=30)
        plt.legend([], frameon=False)
        st.pyplot()

with col2:

    with st.container(border=True):

        # Review Order
        st.header('Review Order')


        total_review_per_index_df = order_reviews_df['review_score'].value_counts(
        ).sort_index().reset_index(name='total_reviews')
        total_review_per_index_df.rename(
            columns={'index': 'rating'}, inplace=True)
        st.write(
            f"Total Reviews: {total_review_per_index_df['total_reviews'].sum()}")
        st.dataframe(total_review_per_index_df)

        plt.figure(figsize=(10, 8))
        plt.pie(
            total_review_per_index_df['total_reviews'],
            labels=total_review_per_index_df['rating'],
            autopct='%1.1f%%',
            startangle=90,
            colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700']
        )
        plt.title('Review Score Distribution', fontsize=20)
        st.pyplot()

    with st.container(border=True):

        # Statistik Order
        st.header('Statistik Order')

        min_date = order_orderItem_orderPayment_df['order_purchase_timestamp'].min(
        )
        max_date = order_orderItem_orderPayment_df['order_purchase_timestamp'].max(
        )

        start_date, end_date = st.date_input(
            'Select Date Range', min_value=min_date, max_value=max_date, value=[min_date, max_date])

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        filtered_order_df = order_orderItem_orderPayment_df[
            (order_orderItem_orderPayment_df['order_purchase_timestamp'] >= start_date) &
            (order_orderItem_orderPayment_df['order_purchase_timestamp'] <= end_date)
        ]

        tab1, tab2 = st.tabs(['Jumlah Order', 'Total Pendapatan'])

        with tab1:
            monthly_orders_df = filtered_order_df.resample(
                'M', on='order_purchase_timestamp').size().reset_index(name='total_orders')
            monthly_orders_df.rename(
                columns={'order_purchase_timestamp': 'month'}, inplace=True)
            monthly_orders_df['month'] = monthly_orders_df['month'].dt.strftime(
                '%Y-%m')
            st.write(
                f"Total Orders: {monthly_orders_df['total_orders'].sum()}")
            st.dataframe(monthly_orders_df)

            plt.figure(figsize=(10, 5))
            plt.plot(monthly_orders_df['month'], monthly_orders_df['total_orders'],
                     marker='o', linestyle='-', color='b')
            plt.title('Monthly Orders' + ' (' + str(start_date.date()) +
                      ' to ' + str(end_date.date()) + ')', fontsize=20)
            plt.xlabel('Month', fontsize=14)
            plt.ylabel('Total Orders', fontsize=14)
            plt.xticks(rotation=45)
            st.pyplot()

        with tab2:
            monthly_payment_df = filtered_order_df.resample('M', on='order_purchase_timestamp')[
                'payment_value'].sum().reset_index(name='total_payment')
            monthly_payment_df.rename(
                columns={'order_purchase_timestamp': 'month'}, inplace=True)
            monthly_payment_df['month'] = monthly_payment_df['month'].dt.strftime(
                '%Y-%m')
            st.write(
                f"Total Payment: {format_currency(monthly_payment_df['total_payment'].sum(), 'BRL', locale='pt_BR')}")
            st.dataframe(monthly_payment_df)

            plt.figure(figsize=(10, 5))
            plt.plot(monthly_payment_df['month'], monthly_payment_df['total_payment'],
                     marker='o', linestyle='-', color='b')
            plt.title('Monthly Payment' + ' (' + str(start_date.date()
                                                     ) + ' to ' + str(end_date.date()) + ')', fontsize=20)
            plt.xlabel('Month', fontsize=14)
            plt.ylabel('Total Payment', fontsize=14)
            plt.xticks(rotation=45)
            st.pyplot()


with st.container(border=True):

    # Demografi Pelanggan
    st.header('Demografi Pelanggan')

    brazil_map = mpimg.imread('./data/brazil_map.png')
    tab1, tab2 = st.tabs(["Customers", "Sellers"])

    with tab1:
        st.subheader('Customer Demographics')
        customer_bystate_df = customer_geolocation_df.groupby(by='customer_state').size(
        ).sort_values(ascending=False).reset_index(name='total_customers')
        customer_bystate_df.rename(
            columns={'customer_state': 'state'}, inplace=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.write(
                f"Total Customers: {customer_bystate_df['total_customers'].sum()}")
            st.dataframe(customer_bystate_df)
        with col2:
            plt.figure(figsize=(12, 6))
            sns.barplot(
                x="total_customers",
                y="state",
                data=customer_bystate_df,
                hue="state",
                palette=['lightcoral'] + ['lightgrey'] *
                    (len(customer_bystate_df) - 1),
                dodge=False
            )
            plt.title('Total Customers by State')
            plt.xlabel('Total Customers')
            plt.ylabel('State')
            plt.legend(loc='center right')
            st.pyplot()
        with col3:
            customer_geolocation_df.plot(kind="scatter", x="geolocation_lng",
                                         y="geolocation_lat", alpha=0.01, figsize=(10, 7), colorbar=False)
            plt.imshow(brazil_map, extent=[-75, -35, -35, 5], alpha=0.5)
            plt.title('Customer Geolocation')
            st.pyplot()

    with tab2:
        st.subheader('Seller Demographics')
        seller_bystate_df = seller_geolocation_df.groupby(by='seller_state').size(
        ).sort_values(ascending=False).reset_index(name='total_sellers')
        seller_bystate_df.rename(
            columns={'seller_state': 'state'}, inplace=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.write(
                f"Total Sellers: {seller_bystate_df['total_sellers'].sum()}")
            st.dataframe(seller_bystate_df)
        with col2:
            plt.figure(figsize=(12, 6))
            sns.barplot(
                x="total_sellers",
                y="state",
                data=seller_bystate_df,
                hue="state",
                palette=['lightcoral'] + ['lightgrey'] *
                    (len(seller_bystate_df) - 1),
                dodge=False
            )
            plt.title('Total Sellers by State')
            plt.xlabel('Total Sellers')
            plt.ylabel('State')
            plt.legend(loc='center right')
            st.pyplot()
        with col3:
            seller_geolocation_df.plot(kind="scatter", x="geolocation_lng",
                                       y="geolocation_lat", alpha=0.01, figsize=(10, 7), colorbar=False)
            plt.imshow(brazil_map, extent=[-75, -35, -35, 5], alpha=0.5)
            plt.title('Seller Geolocation')
            st.pyplot()
