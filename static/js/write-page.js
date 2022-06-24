//Declare all variables
const editBtn = document.querySelector('#edit_btn');
const previewModal = document.querySelector('.preview-modal');
const previewModalContent = document.querySelector('.content-container');
const previewBtn = document.querySelector('.preview-btn');
const userBlogTitleInput = document.querySelector('#blog-title');
const blogTitle = document.querySelector('.review-detail h4');
const blogContent = document.querySelector('.review-detail-content');
let userBlogContentInput;

//ckeditor initiallization
// ClassicEditor.builtinPlugins = [WordCountPlugin]

ClassicEditor
.create(document.querySelector('#toolbar-grouping'), {
    toolbar: [
        'heading', '|',
        'fontfamily', 'fontsize', '|',
        'alignment', '|',
        'fontColor', 'fontBackgroundColor', '|',
        'bold', 'italic', 'underline', '|',
        'link', '|',
        'bulletedList', 'numberedList', '|',
        'outdent', 'indent', '|',
        'uploadImage', 'blockQuote', '|',
        'undo', 'redo'
    ],
    heading: {
        options: [
            { model: 'paragraph', title: 'Paragraph', class: 'ck-heading_paragraph' },
            { model: 'heading1', view: 'h1', title: 'Heading 1', class: 'ck-heading_heading1' },
            { model: 'heading2', view: 'h2', title: 'Heading 2', class: 'ck-heading_heading2' },
            { model: 'heading3', view: 'h3', title: 'Heading 3', class: 'ck-heading_heading3' },
            { model: 'heading4', view: 'h4', title: 'Heading 4', class: 'ck-heading_heading4' },
            { model: 'heading5', view: 'h5', title: 'Heading 5', class: 'ck-heading_heading5' },
            { model: 'heading6', view: 'h6', title: 'Heading 6', class: 'ck-heading_heading6' }
        ]
    },
    // plugins: ['WordCount']
})
.then(e => { 
    userBlogContentInput = () => e.getData();
    // const wordCountPlugin = e.plugins.get( 'WordCount' );
    // console.log(wordCountPlugin);
    // console.log(e.plugins.get("WordCount"));
    // window.editor = e;
    // document.getElementById("demo-word-count").appendChild(e.plugins.get("WordCount").wordCountContainer) 
})
.catch(error => {
    console.error(error);
});


function countChar(val) {
    var len = val.value.length;
    if (len >= 500) {
        val.value = val.value.substring(0, 500);
    } else {
        $('#demo-word-count').text(500 - len);
    }
};

//functions
previewBtn.onclick = () => {
    let content = userBlogContentInput();
    if(userBlogTitleInput.value === '' || userBlogTitleInput.value === null || userBlogTitleInput.value === undefined){
        blogTitle.innerHTML = blogTitle.dataset.placeholder;
        blogTitle.style.color = '#969c8b';  
    } else {
        blogTitle.innerHTML = userBlogTitleInput.value;
        blogTitle.style.color = '#333';  
    }

    if(content === '' || content === null || content === undefined){
        blogContent.innerHTML = blogContent.dataset.placeholder;
        blogContent.style.color = '#969c8b';  
    }else{
        blogContent.innerHTML = content;
        blogContent.style.color = '#444';
    }
    previewModal.style.display = 'flex';
    previewModalContent.style.animation = 'scaleout .3s ease';
}
let closeModal = () => {
    previewModalContent.style.animation = 'scalein .3s ease'
    setTimeout(() => previewModal.style.display = 'none', 250);
}
editBtn.onclick = closeModal;

window.onclick = e => {
    if(e.target === previewModal) closeModal();
}