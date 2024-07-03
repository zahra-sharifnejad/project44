import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title('لیست تماس ها')

# اتصال به گوگل شیت
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Sheet2")

# نمایش دیتافریم با امکان انتخاب
selected_index = st.selectbox('رکورد انتخابی برای ویرایش یا حذف:', df.index, format_func=lambda
    x: f"{df.loc[x, 'نام']} {df.loc[x, 'نام خانوادگی']} - {df.loc[x, 'شماره تماس']}")

if selected_index is not None:
    selected_record = df.loc[selected_index]
    st.write('اطلاعات رکورد انتخابی:')
    st.write(selected_record)

# فرم ویرایش اطلاعات
st.subheader('ویرایش اطلاعات رکورد انتخابی')
name = st.text_input('نام:', selected_record['نام'])
family = st.text_input('نام خانوادگی:', selected_record['نام خانوادگی'])
phone_number = st.text_input('شماره تماس:', selected_record['شماره تماس'])
registration_date = st.date_input('تاریخ:', pd.to_datetime(selected_record['تاریخ']))

# دکمه ویرایش
if st.button('ویرایش'):
    if name and family and phone_number and registration_date:
        df.at[selected_index, 'نام'] = name
        df.at[selected_index, 'نام خانوادگی'] = family
        df.at[selected_index, 'شماره تماس'] = phone_number
        df.at[selected_index, 'تاریخ'] = str(registration_date)
        conn.update(data=df, worksheet="Sheet2")
        st.success('اطلاعات ویرایش شد')
    else:
        st.error('لطفاً تمام اطلاعات را وارد کنید.')

# دکمه حذف
if st.button('حذف'):
    df = df.drop(index=selected_index).reset_index(drop=True)
    conn.update(data=df, worksheet="Sheet2")
    st.success('اطلاعات حذف شد')

# نمایش دیتافریم به روز شده
st.dataframe(df)

# فرم اضافه کردن اطلاعات جدید
st.subheader('وارد کردن اطلاعات جدید')
name_new = st.text_input('نام (جدید):')
family_new = st.text_input('نام خانوادگی (جدید):')
phone_number_new = st.text_input('شماره تماس (جدید):')
registration_date_new = st.date_input('تاریخ (جدید):')

# دکمه ارسال
if st.button('ارسال (جدید)'):
    if name_new and family_new and phone_number_new and registration_date_new:
        new_data = {
            'نام': name_new,
            'نام خانوادگی': family_new,
            'شماره تماس': phone_number_new,
            'تاریخ': str(registration_date_new)
        }
        new_df = pd.DataFrame([new_data])
        df = pd.concat([df, new_df], ignore_index=True)
        conn.update(data=df, worksheet="Sheet2")
        st.success('اطلاعات جدید ذخیره شد')
    else:
        st.error('لطفاً تمام اطلاعات جدید را وارد کنید.')

# نمایش دیتافریم به روز شده
st.dataframe(df)
