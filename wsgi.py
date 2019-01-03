#importing Flask class object from flask library
#import render_template method from flask library
from flask import Flask, render_template

#instantiating Flask object
#__name__ is special and will inherite the name of the python script
application = Flask(__name__)

@application.route('/')
def home():
    #files must live inside a folder called "templates"
    return render_template("home.html")

@application.route('/about/')
def about():
    return render_template("about.html")

@application.route('/plot/')
def plot():
    # https://pandas-datareader.readthedocs.io/en/latest/remote_data.html
    from pandas_datareader import data
    import datetime
    # https://bokeh.pydata.org/en/latest/docs/gallery.html
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2018,1,1)
    end = datetime.datetime(2018,12,31)
    stock_sym = "RHT"

    df = data.DataReader(name=stock_sym, data_source="yahoo", start=start, end=end)

    def inc_dec(o, c):
        if o > c:
            value = "Decrease"
        elif o < c:
            value = "Increase"
        else:
            value = "No Change"
        return value

    df["Status"] = [inc_dec(o, c) for o, c in zip(df.Open, df.Close)]
    df["Middle"] = (df.Open + df.Close)/2
    df["Height"] = abs(df.Close - df.Open)

    p = figure(x_axis_type = 'datetime', width=1000, height=300, title="Candlestick Chart", sizing_mode="scale_width")

    p.grid.grid_line_alpha=0.3
    hours_12 = 12 * 60 * 60 * 1000
    # Add segment glyph first to make sure it shows up behind the boxes
    p.segment(x0=df.index, x1=df.index, y0=df.High, y1=df.Low, color="black")
    # Could also use vbar glyphs here
    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"], hours_12, 
        df.Height[df.Status == "Increase"], fill_color="#D5E1DD", line_color="black")
    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"], hours_12, 
        df.Height[df.Status == "Decrease"], fill_color="#F2583E", line_color="black")

    #output_file(stock_sym + ".html")
    #show(p)

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("plot.html", script1=script1,
    div1=div1, cdn_css=cdn_css, cdn_js=cdn_js)

if __name__ == "__main__":
    application.run(debug=True)


#when using to create requirements.txt, use pip freeze
#to get list of libraries and versions
