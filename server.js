const express = require("express");
const app =express();
const PORT = 5000;
const cors = require('cors');
const fs = require('fs')
let image0 = fs.readFileSync('./images_result/annotated_image0.png', 'base64');
let image1 = fs.readFileSync('./images_result/annotated_image1.png', 'base64');
let image2 = fs.readFileSync('./images_result/annotated_image2.png', 'base64');

const base64Img = require("base64-img");

app.use(cors());
app.all('/*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    next();
});

app.use(express.urlencoded({extended:true}));
app.use(express.json());

app.get("/", function(req, res) {
    return res.send("Server Home")
});

app.post("/api/upload", (req, res) => {
    const imageSrc = req.body.imageSrc;
    const tag = req.body.tag;
    const mode = req.body.mode;
    //console.log(mode)
    base64Img.img(
        imageSrc,
        "./images/",
        `${mode}_${tag}`,
        function (err, filepath) {}
    );
    console.log('img ok')
    return res.json({success: true})
})

let feedbackdata = {d: 1};

app.post("/api/feedback",  (req, res) => {
   const spawn = require('child_process').spawn; // 2. spawn을 통해 "python 파이썬파일.py" 명령어 실행

   const result =  spawn('python3', ['getDriveImageScore.py']); // 3. stdout의 'data'이벤트리스너로 실행결과를 받는다.
    result.stdout.on('data', (data) => {
//     console.log(`stdout: ${data}`);
});

    setTimeout(() => {
        let finalImage0 = { image0 };
        let finalImage1 = { image1 };
        let finalImage2 = { image2 };
        return res.json({success: true, data1: feedbackdata, finalImage0, finalImage1, finalImage2})
    }, 5000)
})

app.post("/api/feedbackdata",  (req, res) => {
    feedbackdata = req.body.resultText;
    console.log(feedbackdata)
    return res.json({success: true});
})

app.listen(PORT, () =>{
    console.log(`Server on localhost:${PORT}`);
})