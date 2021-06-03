from flask import Flask, render_template, request,session
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_e_learning'

mysql = MySQL(app)


@app.route('/')
def index():
    # session["user_id"]=None
    return render_template("home.html")

@app.route('/cart-page')
def cart_page():
    cur = mysql.connection.cursor()
    cur.execute("select product_id from  tbl_cart where user_id=%s", (session["user_id"],))
    cart_products_id = cur.fetchall()
    cur.execute("select * from  tbl_product")
    products = cur.fetchall()
    result=[]
    for id in cart_products_id:
        for p in products:
            if id[0] == p[0]:
                result.append(p)

    mysql.connection.commit()
    return render_template("cart.html",products=result)

@app.route('/books')
def books():
    return render_template("Maths_book.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/submit',methods=['POST'])
def submit():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_user(name,email,password) VALUES (%s, %s,%s)", (name, email,password))
        mysql.connection.commit()
        msg= 'Signup Successfully'
        return render_template("signup.html",msg=msg)

@app.route('/login-submit',methods=['POST'])
def submit_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute("select id from  tbl_user where email=%s and password=%s",(email,password))
        mysql.connection.commit()
        user_id = cur.fetchone()
        cur.close()
        if user_id is not None:
             session["user_id"] = user_id[0]
             print(session["user_id"])
             return render_template("home1.html")
        else:
            return "sign In Failed , maybe wrong username or password"

@app.route('/signin')
def signin():
    return render_template("signin.html")


@app.route('/add-to-cart/<int:id>')
def cart(id):
    if session.get("user_id") is None:
        return render_template("signin.html")
    else:
        user_id =session.get("user_id")
        cur = mysql.connection.cursor()
        check=cur.execute("select 1 from  tbl_cart where product_id=%s and user_id=%s ",(id,user_id))
        if check:
            check=0
        else:
            cur.execute("INSERT into tbl_cart (product_id,user_id) VALUES (%s,%s)", (id,user_id))

        mysql.connection.commit()
        msg = 'Added to Cart Successfully'
        return render_template("Maths_book.html",msg=msg)

@app.route('/remove-to-cart/<int:id>')
def remove_cart(id):
        cur = mysql.connection.cursor()
        cur.execute("delete from  tbl_cart where product_id=%s",(id,))
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("select product_id from  tbl_cart where user_id=%s", (session["user_id"],))
        cart_products_id = cur.fetchall()
        cur.execute("select * from  tbl_product")
        products = cur.fetchall()
        result = []
        for id in cart_products_id:
            for p in products:
                if id[0] == p[0]:
                    result.append(p)
                    print(p)
        mysql.connection.commit()
        return render_template("cart.html", products=result)

@app.route('/contact_us')
def contact_us():
      return  render_template("contact.html")

@app.route('/course')
def course():
    cur = mysql.connection.cursor()
    cur.execute("select * from  tbl_course")
    courses = cur.fetchall()
    return  render_template("course.html",courses=courses,)
@app.route('/quiz/<int:id>')
def quiz(id):
    cur = mysql.connection.cursor()
    cur.execute("select * from  tbl_ques where course_id = %s ",(id,))
    questions = cur.fetchall()
    return render_template("quiz.html",questions=questions)



if __name__ == '__main__':
    app.run(debug=True)