const OnRequest = () => {
    const parent = document.querySelector('.main');
    let wrapper = document.querySelector('.main .content') 
    if (wrapper !== null) {
        pre_result = document.querySelector('.result');
        wrapper.removeChild(pre_result);
    } else {
        const result_title = document.createElement('h3');
        wrapper = document.createElement('div');

        result_title.innerText = "生成結果";
        wrapper.classList.toggle("content");
        wrapper.appendChild(result_title);
        parent.appendChild(wrapper);
    }

    return wrapper;
}

const OnGetResult = (filename, wrapper) => {
    const image_src = `/static/tmp/${filename}`;
    const parent = wrapper;
    const img = document.createElement('img');
    img.setAttribute("src", image_src);
    img.classList.toggle("result");

    parent.appendChild(img);
}

document.addEventListener("DOMContentLoaded",function(){
    const sbt = document.querySelector('button[type="submit"]');
    const load_anim = document.querySelector('.anim');

    const OnSubmitted = () => {
        console.log("sbt clicked");
        load_anim.style.display = 'block';
        const fileField = document.querySelector('input[type="file"]');
        const formData = new FormData();
        
        formData.append('image', fileField.files[0]);
        const wrapper = OnRequest(); 
        console.log(wrapper);
        fetch('/pixelation', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            OnGetResult(result["filename"], wrapper);
            console.log('Success:', result);
            load_anim.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            load_anim.style.display = 'none';
        });
        
    }
    
    sbt.onclick = OnSubmitted;
});