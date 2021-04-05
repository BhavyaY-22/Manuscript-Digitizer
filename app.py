from flask import Flask, render_template, request, send_file
import os
import easyocr
from IPython.display import Image
from os import listdir
from os.path import isfile, join
import numpy
import cv2

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route("/")
def index():
    if os.path.isdir('tmp/'):
        for filename in os.listdir('tmp/'):
            os.remove('tmp/' + filename)
    if os.path.isfile('output.txt'):
        os.remove('output.txt')
    return render_template("index.html")

@app.route("/upload", methods=["POST","GET"])
def upload():
    return render_template("upload.html")


def vconcat_resize(img_list, interpolation = cv2.INTER_CUBIC):
      # take minimum width
    w_min = min(img.shape[1] 
                for img in img_list)
      
    # resizing images
    im_list_resize = [cv2.resize(img,
                      (w_min, int(img.shape[0] * w_min / img.shape[1])),
                                 interpolation = interpolation)
                      for img in img_list]
    # return final image
    return cv2.vconcat(im_list_resize)

@app.route("/process", methods=["POST","GET"])
def process():
    target = os.path.join(APP_ROOT,'tmp/')
    if not os.path.isdir(target):
        os.mkdir(target)
    
    for file in request.files.getlist("file"):
        filename = file.filename
        dest = "/".join([target, filename])
        file.save(dest)
    
    onlyfiles = [ f for f in listdir(target) if isfile(join(target,f)) ]
    images = numpy.empty(len(onlyfiles), dtype=object)
    for n in range(0, len(onlyfiles)):
        images[n] = cv2.imread( join(target,onlyfiles[n]) )
  



    img_v_resize = vconcat_resize([images[n] for n in range(0, len(onlyfiles))] )  
    # show the output image
    f = target+'vconcat_resize.jpg'
    cv2.imwrite(f, img_v_resize)
    i = request.form.get("language")
    reader = easyocr.Reader([i])
    # image file to be extracted
    
    
    Image(f)
    # extracted text
    ot = reader.readtext(f, detail=0)
    otext = ' '.join([str(elem) for elem in ot])
    encoded_unicode = otext.encode("utf8")
    a_file = open("output.txt", "wb")
    a_file.write(encoded_unicode)
    a_file = open("output.txt", "r")
    return render_template("upload.html")

@app.route("/download", methods=["GET"])
def download():
    p = "output.txt"
    return send_file(p,as_attachment=True)

@app.route("/inform", methods=["POST","GET"])
def inform():
    return render_template("Help.html")
@app.route("/feedback", methods=["POST","GET"])
def feedback():
    return render_template("Contact.html")

@app.route("/archives", methods=["POST","GET"])
def archives():
    return render_template("archive.html")


@app.route("/arc_hi", methods=["GET"])
def arc_hi():
    p = "hindi.txt"
    return send_file(p,as_attachment=True)

@app.route("/arc_te", methods=["GET"])
def arc_te():
    p = "telugu.txt"
    return send_file(p,as_attachment=True)

@app.route("/arc_ta", methods=["GET"])
def arc_ta():
    p = "tamil.txt"
    return send_file(p,as_attachment=True)

@app.route("/arc_be", methods=["GET"])
def arc_be():
    p = "bengali.txt"
    return send_file(p,as_attachment=True)

@app.route("/arc_mr", methods=["GET"])
def arc_mr():
    p = "marathi.txt"
    return send_file(p,as_attachment=True)

@app.route("/arc_ar", methods=["GET"])
def arc_ar():
    p = "arabic.txt"
    return send_file(p,as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
    
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
