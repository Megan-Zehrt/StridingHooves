function getBase64Image(img) {
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);
    var dataURL = canvas.toDataURL("image/png");
    return dataURL.replace(/^data:image\/?[A-z]*;base64,/);
  }
  
  var base64 = getBase64Image(document.getElementById("imageid"));

function ChangeImage1(){
    var video = document.getElementById("video");
    video.src="{{url_for('.static', filename='images/polework_video.mp4')}}";
    return false;
}

function changeImageToVideo() {
  var image = document.getElementById('image');
  var video = document.getElementById('video');
  image.style.display = 'none';
  video.style.display = 'block';
  video.src = "{{ url_for('.static', filename='images/polework_video.mp4') }}";
}

function myFunction() {
  var popup = document.getElementById("myPopup");
  popup.classList.toggle("show");
}

function myFunctionRider() {
  var popup = document.getElementById("myPopupRider");
  popup.classList.toggle("show");
}

function myFunctionHorse() {
  var popup = document.getElementById("myPopupHorse");
  popup.classList.toggle("show");
}

function myFunctionHamburger() {
  var x = document.getElementById("myLinks");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
  }
}