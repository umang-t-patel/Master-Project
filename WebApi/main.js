var CV_URL = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyB-6sBC7SdFm4cd5pQxIuolRqGZ2ggNWx4';

$(function () {
  $('#fileform').on('submit', uploadFiles);
});

/**
 * 'submit' event handler - reads the image bytes and sends it to the Cloud
 * Vision API.
 */
function uploadFiles (event) {
  event.preventDefault(); // Prevent the default form post

  // Grab the file and asynchronously convert to base64.
  var file = $('#fileform [name=fileField]')[0].files[0];
  var reader = new FileReader();
  reader.onloadend = processFile;
  reader.readAsDataURL(file);
}

/**
 * Event handler for a file's data url - extract the image data and pass it off.
 */
function processFile (event) {
  var content = event.target.result;
  sendFileToCloudVision(content.replace('data:image/jpeg;base64,', ''));
}

/**
 * Sends the given file contents to the Cloud Vision API and outputs the
 * results.
 */
function sendFileToCloudVision (content) {
  var type = $('#fileform [name=type]').val();

  // Strip out the file prefix when you convert to json.
  var request = {
    requests: [{
     image: {
       source: {
         gcsImageUri: "gs://visionapiusinghtml/1.jpg"
       }
     },
	 
      // image: {
        // content: content
      // },
      features: [{
        type: "FACE_DETECTION",
        maxResults: 200
      },{
        type: "LABEL_DETECTION",
        maxResults: 200
      },{
        type: "TEXT_DETECTION",
        maxResults: 200
      },{
        type: "LANDMARK_DETECTION",
        maxResults: 200
      },{
        type: "LOGO_DETECTION",
        maxResults: 200
      },
	  ]
    }]
  };

  $('#results').text('Loading...');
  $.post({
    url: CV_URL,
    data: JSON.stringify(request),
    contentType: 'application/json'
  }).fail(function (jqXHR, textStatus, errorThrown) {
    $('#results').text('ERRORS: ' + textStatus + ' ' + errorThrown);
  }).done(displayJSON);
}

/**
 * Displays the results.
 */
function displayJSON (data) {
  var contents = JSON.stringify(data, null, 4);
  $('#results').text(contents);
  var evt = new Event('results-displayed');
  evt.results = contents;
  document.dispatchEvent(evt);
}
