let scene, camera, renderer, model;

function initViewer() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer();
    
    const viewer = document.getElementById('viewer');
    renderer.setSize(viewer.clientWidth, viewer.clientHeight);
    viewer.appendChild(renderer.domElement);
    
    // 设置相机位置
    camera.position.z = 5;
    
    // 添加环境光
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    // 添加方向光
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(0, 1, 0);
    scene.add(directionalLight);
    
    animate();
}

function animate() {
    requestAnimationFrame(animate);
    if (model) {
        model.rotation.y += 0.01;
    }
    renderer.render(scene, camera);
}

async function uploadImage() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    
    document.getElementById('loading').style.display = 'block';
    
    try {
        const response = await fetch('/upload/', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('Upload failed');
        
        const data = await response.json();
        loadModel(data.filename);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to convert image to 3D model');
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function loadModel(filename) {
    const loader = new THREE.PLYLoader();
    loader.load(`/model/${filename}`, function(geometry) {
        if (model) scene.remove(model);
        
        const material = new THREE.MeshStandardMaterial({
            color: 0xffffff,
            vertexColors: true
        });
        
        model = new THREE.Mesh(geometry, material);
        scene.add(model);
    });
}

// 初始化3D查看器
initViewer();