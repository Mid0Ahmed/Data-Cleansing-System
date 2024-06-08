from flask import Flask ,request,render_template,url_for,redirect
import pandas as pd
import os
from missing_value import handle_missing,get_uploaded_files,pers_missing,find_missing_values_rows
from duplicates import find_duplicate_rows,get_column_names,pers_duplicate,remove_duplicates_and_save
# from outliers import getOutliersDetails,getNegative,remove_negative_rows,remove_outliers_and_save,save_and_display_plot

# from conver import get_sql_server_databases,db_convert,get_server_name
# from dashboard import calculate_null_percentage_in_database
# from outliers import getOutliersDetails

app=Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def Auth():
    return render_template('Auth.html')



@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/About')
def About():
    return render_template('About.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')






#################################################Missing###########################

@app.route('/Missing', )
def miss():
  filenames=get_uploaded_files()
  if request.method == 'POST':
    operation = request.form['operation']
    filename = request.form['table']
    if filename=="Not select":
      return render_template('Missing_value.html', filenames=filenames,table_original="You haven't selected any Table!",missingPers=0,missingCount=0,totalRows=0)
    else:
      df = pd.read_csv('uploads/'+filename)
        
      if (operation=='show'):


        return render_template('Missing_value.html')
      elif (operation=='fill'):
        intType = request.form['fill-int-type']
        if intType=='Not select int':
          return render_template('Missing_value.html',intmsg='Select Option To Fill Integer Missing Value',missingPers=0,missingCount=0,totalRows=0)
        else:   
          strValue = request.form['fill-str-value']
          if strValue=='':
            return render_template('Missing_value.html',strmsg='Select Option To Fill String Missing Value',missingPers=0,missingCount=0,totalRows=0)
          else:   
            newdata=handle_missing(df,intType,strValue)
            newdata.to_csv("uploads/"+filename,index=False)
            table_html_cleaned = newdata.to_html(classes='table table-bordered table-striped ', index=False)

            return render_template('Missing_value.html', table_original=table_html_original, table_cleaned=table_html_cleaned,filenames=filenames,missingPers=missingPers,missingCount=missingCount,totalRows=totalRows)
      elif operation=='delete' :
       df=df.dropna()
       df.to_csv('uploads/'+filename)
       missingPers,missingCount,totalRows=pers_missing(df)
       table_html_original = df.to_html(classes='table table-bordered table-striped ', index=False)

       return render_template('Missing_value.html', table_original=table_html_original,table_cleaned="No Missing Value Found.!", filenames=filenames,missingPers=missingPers,missingCount=missingCount,totalRows=totalRows)
      # if (operation=='Not select int'):

      #   missingPers,missingCount,totalRows,missing_Html_Table,table_html_original=show()
      #   return render_template('Missing_value.html', table_original=table_html_original, table_cleaned=missing_Html_Table,filenames=filenames,missingPers=missingPers,missingCount=missingCount,totalRows=totalRows,intmsg='Select Option To Fill Integer Missing Value')
  else:
      return render_template('Missing_value.html', filenames=filenames,missingPers=0,missingCount=0,totalRows=0)




###############################endMissing###########################





################################Duplicate###########################


@app.route('/duplicate',methods=['POST', 'GET'])
def duplicate():
    filenames=get_uploaded_files()
    if request.method == 'POST':
        operation = request.form['operation']
        filename = request.form['table']
        if filename=="Not select":
          return render_template('duplicate.html', filenames=filenames,table_original="You haven't selected any Table!",pers=0,effectedRows=0,totalRows=0)
        else:
          def show_dupl():
                  selected_columns = request.form.getlist('columns')
                  filename = request.form['table']
                  df = pd.read_csv('uploads/'+filename)
                  pers,effectedRows,totalRows=pers_duplicate(df)
                  columns=get_column_names(df)
                  if selected_columns:
                    show_dup=find_duplicate_rows(df,selected_columns)
                    pers,effectedRows,totalRows=pers_duplicate(df,selected_columns)
                  else:
                    show_dup=find_duplicate_rows(df,'all')


                  if show_dup.count().max() ==0:
                      table_html_duplicate='No Duplicates Found.'
                  else:
                      table_html_duplicate = show_dup.to_html(classes='table table-striped table-bordered sizee ', index=False)
                  table_html_original = df.to_html(classes='table table-striped table-bordered sizee', index=False)
                  return pers,effectedRows,totalRows,table_html_original,table_html_duplicate,columns,selected_columns
          if operation == 'show':
            pers,effectedRows,totalRows,table_html_original,table_html_duplicate,columns,selected_columns=show_dupl()
            return render_template('duplicate.html',filenames=filenames,table_original=table_html_original,table_duplicate=table_html_duplicate,pers=pers,effectedRows=effectedRows,totalRows=totalRows,columns=columns,selected_columns=selected_columns)
          else:
            try:
              selected_columns = request.form.getlist('columns')
              if selected_columns:
                remove_duplicates_and_save(filename,selected_columns)
                pers,effectedRows,totalRows,table_html_original,table_html_duplicate,columns,selected_columns=show_dupl()
                return render_template('duplicate.html',filenames=filenames,table_original=table_html_original,table_duplicate=table_html_duplicate,pers=pers,effectedRows=effectedRows,totalRows=totalRows)
              else:
                 remove_duplicates_and_save(filename,'all')
                 pers,effectedRows,totalRows,table_html_original,table_html_duplicate,columns,selected_columns=show_dupl()
                 return render_template('duplicate.html',filenames=filenames,table_original=table_html_original,table_duplicate=table_html_duplicate,pers=pers,effectedRows=effectedRows,totalRows=totalRows)
            except:
               pers,effectedRows,totalRows,table_html_original,table_html_duplicate=show_dupl()
               return render_template('duplicate.html',filenames=filenames,table_original=table_html_original,table_duplicate=table_html_duplicate,pers=pers,effectedRows=effectedRows,totalRows=totalRows)
          
          
    return render_template('duplicate.html',filenames=filenames,pers=0,effectedRows=0,totalRows=0)
    
    


#################################################endDuplicate###########################




###############################outlier###########################

@app.route('/outlier')
def outlier():
    filenames=get_uploaded_files()
    if request.method == 'POST':
        filename = request.form['table']
        operation = request.form['operation']
        def show_outlier(filename):
           df = pd.read_csv('uploads/'+filename)
           columns=get_column_names(df)
           table_html_original = df.to_html(classes='table table-striped table-bordered ', index=False)
           table_html_original = df.to_html(classes='table table-striped table-bordered ', index=False)
           if outliers.count().max() ==0:
               return render_template('outlier.html',filenames=filenames,table_original=table_html_original,table_outliers="No Outlier Found!",total_rows=total_rows,num_outliers=num_outliers,outlier_percentage=outlier_percentage,columns=columns)
           else:
             table_html_outliers = outliers.to_html(classes='table table-striped table-bordered ', index=False)
             return render_template('outlier.html',filenames=filenames,table_original=table_html_original,table_outliers=table_html_outliers,total_rows=total_rows,num_outliers=num_outliers,outlier_percentage=outlier_percentage,columns=columns)
                        
           

        if  filename=='Select':
            return render_template('outlier.html',filenames=filenames,table_original="You Should Select Table !",total_rows=0,num_outliers=0,outlier_percentage=0)
        else:   



              if operation == 'show':
                      df = pd.read_csv('uploads/'+filename)
                      columns=get_column_names(df)
                      table_html_original = df.to_html(classes='table table-striped table-bordered ', index=False)
                      return render_template('outlier.html',filenames=filenames,table_original=table_html_original,total_rows=0,num_outliers=0,outlier_percentage=0,columns=columns)

              elif operation == 'find_outlier':
                      df = pd.read_csv('uploads/'+filename)
                      columns=get_column_names(df)
                      chart = request.form['chart']
                      selected_columns = request.form.getlist('columns')
                      

                      table_html_original = df.to_html(classes='table table-striped table-bordered ', index=False)
                      if selected_columns:

                        if outliers.count().max() ==0:
                            return render_template('outlier.html',filenames=filenames,table_original=table_html_original,table_outliers="No Outlier Found!",total_rows=total_rows,num_outliers=num_outliers,outlier_percentage=outlier_percentage,columns=columns)
                        else:
                           
                          table_html_outliers = outliers.to_html(classes='table table-striped table-bordered ', index=False)
                          return render_template('outlier.html',filenames=filenames,table_original=table_html_original,table_outliers=table_html_outliers,total_rows=total_rows,num_outliers=num_outliers,outlier_percentage=outlier_percentage,columns=columns)
                        
                      else:
                        return render_template('outlier.html',filenames=filenames,table_original=table_html_original,table_outliers="You Don`t Select Any Row!",total_rows=0,num_outliers=0,outlier_percentage=0,columns=columns)
              elif operation == 'negative':
                      df = pd.read_csv('uploads/'+filename)
                      columns=get_column_names(df)

                      selected_columns = request.form.getlist('columns')
                      table_html_original = df.to_html(classes='table table-striped table-bordered ', index=False)
                      if selected_columns:
                        outliers,total_rows,num_outliers,outlier_percentage=[0]
                        if outliers.count().max() ==0:
                            return render_template('outlier.html',filenames=filenames,table_original=table_html_original,table_outliers="No Negative Value Found!",total_rows=total_rows,num_outliers=num_outliers,outlier_percentage=outlier_percentage,columns=columns)
                        else:
                           
                          table_html_outliers = outliers.to_html(classes='table table-striped table-bordered ', index=False)
                          return render_template('outlier.html',filenames=filenames,table_original=table_html_original,table_outliers=table_html_outliers,total_rows=total_rows,num_outliers=num_outliers,outlier_percentage=outlier_percentage,columns=columns)
                      else:
                        return render_template('outlier.html',filenames=filenames,table_original=table_html_original,table_outliers="You Don`t Select Any Row!",total_rows=0,num_outliers=0,outlier_percentage=0,columns=columns)
              elif operation == 'delete_outlier':
                      selected_columns = request.form.getlist('columns')
                      df = pd.read_csv('uploads/'+filename)
                      columns=get_column_names(df)
                      if selected_columns:
                         return  show_outlier(filename)
              elif operation == 'delete_negative':
                      selected_columns = request.form.getlist('columns')
                      df = pd.read_csv('uploads/'+filename)
                      columns=get_column_names(df)
                      if selected_columns:
                         return  show_outlier(filename)
                    

        
    else:
        return render_template('outlier.html',filenames=filenames,total_rows=0,num_outliers=0,outlier_percentage=0)



###############################endoutlier###########################



@app.route('/invalid')
def invalid():
    return render_template('invalid_format.html')




  
if  __name__=='__main__':
    app.run(debug=False,port=2020)
