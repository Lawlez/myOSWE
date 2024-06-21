const express = require('express');
const app = express();
const tf = require('@tensorflow/tfjs-node');
const port = 3000;

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Car Track ML</title>
    <style>
        canvas { border: 1px solid black; }
    </style>
    </head>
    <body>
    <canvas id="trackCanvas" width="500" height="500"></canvas>
    <script>
    const canvas = document.getElementById('trackCanvas');
    const ctx = canvas.getContext('2d');

    function drawTrack() {
        ctx.fillStyle = 'gray';
        ctx.fillRect(100, 100, 300, 300); // Draw square track
        ctx.beginPath();
        ctx.arc(100, 100, 50, 0, Math.PI / 2, false); // Rounded corner
        ctx.fill();
    }

    function drawCar(x, y) {
        ctx.fillStyle = 'red';
        ctx.fillRect(x, y, 24, 36); // Car dimensions in canvas scale
    }

    function update() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawTrack();
        drawCar(150, 150); // Initial car position, change as needed
        requestAnimationFrame(update); // Loop to animate
    }

    update();
    </script>
    </body>
    </html>
    `);
});

// TensorFlow Model
function createModel() {
    const model = tf.sequential();
    model.add(tf.layers.dense({inputShape: [4], units: 24, activation: 'relu'}));
    model.add(tf.layers.dense({units: 24, activation: 'relu'}));
    model.add(tf.layers.dense({units: 4, activation: 'softmax'})); // 4 outputs: forward, backward, left, right
    
    return model;
}

const model = createModel();
model.compile({optimizer: 'adam', loss: 'categoricalCrossentropy'});

// Dummy training function to illustrate
function trainModel() {
    const xs = tf.tensor2d([[0.5, 0.5, 0.1, 0.0]]);
    const ys = tf.tensor2d([[1, 0, 0, 0]]);
    
    model.fit(xs, ys, {
        epochs: 10,
        callbacks: {
            onEpochEnd: (epoch, log) => console.log(`Epoch ${epoch}: loss = ${log.loss}`)
        }
    });
}

// Call train model to demonstrate (you'd normally trigger this appropriately)
trainModel();

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
