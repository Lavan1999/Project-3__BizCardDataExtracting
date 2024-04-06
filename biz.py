import pandas as pd 
import psycopg2
import easyocr
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
import re
import streamlit as st
import numpy as np
from psycopg2 import OperationalError
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData,update



# Creating a database engine
engine = create_engine("postgresql+psycopg2://postgres:Lavan123@localhost/bizcardx")
# Creating a connection
conn = engine.connect()
# Reflecting the existing database schema
metadata = MetaData()
metadata.reflect(bind=engine)
# Accessing the 'business_card' table from the reflected metadata
biz_card_table = Table('biz_card', metadata, autoload_with=engine)

#Streamlit page setting
st.set_page_config(layout='wide')

#('## :green[Enter the channel ID]')
st.title(" :blue[BizCard: Extracting Business Card Data with OCR]")

col1,col2 = st.columns([1,4])
with col1:
    option = st.radio("",
        ["Home Page", "Upload the card and Extract text", "Modify Details"])
    if option =="Modify Details":
        option1 = st.radio("", ["Modify","Delete"])

    # Initializing EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False)


# 1 Home page setup
if option == 'Home Page':
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### :green[**Technologies Used :**] In this Streamlit web app, users can upload images of business cards to extract relevant information using EasyOCR. Once uploaded, the app provides options to view, modify, or delete the extracted data. Additionally, users can save the extracted information along with the uploaded business card image into a database. The database supports multiple entries, allowing users to store and manage information from various business cards.")
        st.markdown("#### :green[**Used Tools**] Python, easy OCR, Streamlit, SQL, Pandas")
    with col2:
        st.image("C:/Users/DELL/Downloads/biz card.jpg", width =500 )


try:
    # Connecting to PostgreSQL server
    with psycopg2.connect(host='localhost', user='postgres', password='Lavan123', database='bizcardx', port=5432) as mydb:
        mycursor = mydb.cursor()

        # Create table if not exists
        mycursor.execute('''Create table if not exists biz_cardz
                            (id SERIAL PRIMARY KEY,
                            name TEXT,
                            company_name TEXT,
                            designation TEXT,
                            mobile_number VARCHAR(50),
                            email TEXT,
                            website TEXT,
                            street TEXT,
                            city TEXT,
                            state TEXT,
                            pin_code VARCHAR(10),
                            image BYTEA)''')
        # Committing the changes
        mydb.commit()
        print("Table 'biz_card' created successfully.")

except OperationalError as e:
    print(f"Error: {e}")
    
# Connection for sqlAlchemy



if option =='Upload the card and Extract text':
    
    with col2:
        st.markdown(" :green[Upload Your Business Card]")
        selected_card = st.file_uploader("Upload business card here", label_visibility="collapsed",
                                         type=["png", "jpeg", "jpg"])

    if selected_card is not None:
        
        #easy OCR
        saved_img = os.getcwd()+ "\\" + "uploaded_card"+ "\\"+ selected_card.name
        text_result = reader.readtext(saved_img, detail = 0,paragraph=False)
        
        
        # Converting image to binary to upload to SQL database
        def binary(file):
            # Convert image data to binary format
            with open(file, 'rb') as file:
                binaryData = file.read()
            return binaryData
        
        details = {"name" : [],
                "company_name" : [],
                "designation" : [],
                "mobile_number" :[],
                "email" : [],
                "website" : [],
                "street" : [],
                "city" : [],
                "state" : [],
                "pin_code" : [],
                "image" : binary(saved_img)
               }
        
        def extract_text(text):
            
            for idx,item in enumerate(text):
                
                # 1-To get card holder name
                if idx == 0:
                    details["name"].append(item)
                    
                # 2-To get company name  
                elif idx == len(text)-1:
                    details["company_name"].append(item)
                    
                # 3-To get designation
                elif idx == 1:
                    details["designation"].append(item)
                    
                # 4-To get mobile number
                elif "-" in item:
                    details["mobile_number"].append(item)
                    if len(details["mobile_number"]) ==2:
                        details["mobile_number"] = " & ".join(details["mobile_number"])
                        
                # 5-To get email ID
                elif "@" in item:
                    details["email"].append(item)
                
                # 6-To get website url
                elif "www " in item.lower() or "www." in item.lower():
                    details["website"].append(item)
                elif "WWW" in item:
                    details["website"] = text[4] +"." + text[5]
                                    
                # 7-To get area
                if re.findall('^[0-9].+, [a-zA-Z]+',item):
                    details["street"].append(item.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+',item):
                    details["street"].append(item) 
                    
                # 8-To get city name
                match1 = re.findall('.+St , ([a-zA-Z]+).+', item)
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', item)
                match3 = re.findall('^[E].*',item)
                if match1:
                    details["city"].append(match1[0])
                elif match2:
                    details["city"].append(match2[0])
                elif match3:
                    details["city"].append(match3[0])
                    
                # 9-To get state
                state_match = re.findall('[a-zA-Z]{9} +[0-9]',item)
                if state_match:
                     details["state"].append(item[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);',item):
                    details["state"].append(item.split()[-1])
                if len(details["state"])== 2:
                    details["state"].pop(0)
                    
                # 10-To get pincode        
                if len(item)>=6 and item.isdigit():
                    details["pin_code"].append(item)
                elif re.findall('[a-zA-Z]{9} +[0-9]',item):
                    details["pin_code"].append(item[10:])
        extract_text(text_result)
        
        

        def image_preview(image,res): 
            for (box, text, prob) in res: 
              # unpack the bounding box
                (top_left, top_right, bottom_right, bottom_left) = box
                top_left = (int(top_left[0]), int(top_left[1]))
                top_right = (int(top_right[0]), int(top_right[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
                cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
            plt.rcParams['figure.figsize'] = (15,15)
            plt.axis('off')
            plt.imshow(image) 
            
        col3,col4 = st.columns(2,gap="large")
        with col3:
            st.markdown("#     ")
            with st.spinner("Please wait processing image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img = os.getcwd()+ "\\" + "uploaded_card"+ "\\"+ selected_card.name
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                st.header(" :blue[Image Processed and Data Extracted]")
                st.pyplot(image_preview(image,res))  
                
            # Display the extracted text   
            with col4:
                st.markdown("#     ")
                st.markdown("#     ")
                for box, text, prob in res:
                    st.write(f"Text  : {text}")
    
        df = pd.DataFrame(details)
        st.write(df)
        
        if st.button("Upload to Database"):
            for i, row in df.iterrows():
                # Check if the company_name already exists in the table
                sql_check = "SELECT COUNT(*) FROM biz_card WHERE name = %s"
                mycursor.execute(sql_check, (row['name'],))
                result = mycursor.fetchone()

                if result[0] > 0:
                    # If company_name already exists, mark it as 'already exist'
                    st.warning(f"{row['name']} card already exists in the database")
                else:
                    # If company_name doesn't exist, insert into the table
                    sql_insert = """INSERT INTO biz_card(company_name, name, designation, mobile_number, email, website,street, city, state, pin_code, image)
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    mycursor.execute(sql_insert, tuple(row))
                    mydb.commit()

                    st.success("Uploaded to database successfully!")
 

if option == "Modify Details":
    with col2:
        # Read data from the 'biz_card' table into a DataFrame
        df = pd.read_sql('biz_card', engine)      
        st.write(' :green[Database Table]')             
        st.dataframe(df)
        st.button('Show Changes')
        
        
        if option1 =="Modify":
            col3, col4 = st.columns(2)
            with col3:
                st.write(' :green[Select which card you want to change]')
                names= ['Please select one','id','name','email']
                selected = st.selectbox('',names)
                if selected != 'Please select one':
                        select = ['Please select one'] + list(df[selected])
                        select_detail = st.selectbox(f'**Select the {selected}**', select)
                        with col4:
                            if select_detail != 'Please select one':
                                st.write(' :green[Choose what details to modify]')
                                df1 = df[df[selected] == select_detail]
                                df1 = df1.reset_index()
                                select_modify = st.selectbox('', ['Please select one'] + list(df.columns))
                                if select_modify != 'Please select one':
                                    a = df1[select_modify][0]            
                                    st.write(f'Do you want to change {select_modify}: **{a}** ?')
                                    modified = st.text_input(f'**Enter the {select_modify} to be modified.**')
                                    if modified:
                                        st.write(f'{select_modify} **{a}** will change as **{modified}**')
                                    with col3:
                                        if st.button("Commit Changes"):
                                            # Define the update statement
                                            update_statement = (
                                                                update(biz_card_table)
                                                                .where(biz_card_table.c[selected] == select_detail)
                                                                .values({select_modify: modified})
                                                            )
                                            # Executing the update statement
                                            conn.execute(update_statement)
                                            conn.commit()
                                            st.success("Changes committed successfully!")

        
        if option1 == 'Delete':
            col3, col4 = st.columns(2)
            with col3:
                st.write(' :green[Select where to delete the details]')
                names= ['Please select one','name','email']
                delete_selected = st.selectbox('',names) 
                if delete_selected != 'Please select one':
                    select = df[delete_selected]
                    delete_select_detail = st.selectbox(f'**Select the {delete_selected} to remove**', ['Please select one'] + list(select))
                    if delete_select_detail != 'Please select one':
                        st.write(f'Do you want to delete **{delete_select_detail}** card details ?')
                        col5,col6,col7 =st.columns([1,1,5])
                        delete = col5.button('Yes I do')
                        if delete:
                            delete_query = (
                                            biz_card_table.delete()
                                            .where(biz_card_table.c[delete_selected] == delete_select_detail)
                                            )

                            # Execute the delete statement
                            conn.execute(delete_query)
                            conn.commit()
                            st.success("Data Deleted successfully", icon ='✅')

        
    
    
    
    