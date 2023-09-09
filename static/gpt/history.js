let history_arr

function create_history_box(id, input_value, sidebar_datetime) {
    let history_container = document.getElementById('history')
    // 1. create history box
    let history_box = document.createElement('div')
    history_box.setAttribute('id', "box" + id)
    history_box.setAttribute('class', 'history_box')
    history_container.appendChild(history_box)
    // 2. create history input
    let history_input = document.createElement('input')
    history_input.value = input_value
    history_input.setAttribute('disabled', '')
    history_input.setAttribute('class', 'left history_input')
    history_box.appendChild(history_input)
    // 3. create history sidebar
    let history_sidebar = document.createElement('div')
    history_sidebar.innerText = sidebar_datetime
    history_sidebar.setAttribute('class', 'right history_sidebar')
    history_box.appendChild(history_sidebar)
    // 4. create opt
    let history_opt = document.createElement('div')
    history_opt.setAttribute('class', 'right history_sidebar none')
    history_box.appendChild(history_opt)
    // 5. create del_div
    let del_div = document.createElement('div')
    del_div.setAttribute('class', 'opt_div center')
    history_opt.appendChild(del_div)
    // 6. create del_img
    let del_img = document.createElement('img')
    del_img.setAttribute('src', '../static/img/delete.svg')
    del_img.setAttribute('alt', 'delete')
    del_img.setAttribute('class', 'opt_img')
    del_div.appendChild(del_img)
    // 7. create modify_div
    let mod_div = document.createElement('div')
    mod_div.setAttribute('class', 'opt_div center')
    history_opt.appendChild(mod_div)
    // 8. create modify_img
    let mod_img = document.createElement('img')
    mod_img.setAttribute('src', '../static/img/modify.svg')
    mod_img.setAttribute('alt', 'modify')
    mod_img.setAttribute('class', 'opt_img')
    mod_div.appendChild(mod_img)
    // 9. create more_div
    let more_div = document.createElement('div')
    more_div.setAttribute('class', 'opt_div center')
    history_opt.appendChild(more_div)
    // 10. create more_img
    let more_img = document.createElement('img')
    more_img.setAttribute('src', '../static/img/more.svg')
    more_img.setAttribute('alt', 'more')
    more_img.setAttribute('class', 'opt_img')
    more_div.appendChild(more_img)

    return history_box
}

function mouse_enter(box, input, sidebar, opt) {
    box.addEventListener("mouseenter", () => {
        box.setAttribute('class', 'history_box mouse_enter_box')
        input.setAttribute('class', 'left history_input mouse_enter_input')
        sidebar.setAttribute('class', 'right history_sidebar none')
        opt.setAttribute('class', 'right history_sidebar')

    })
}

function mouse_leave(box, input, sidebar, opt) {
    box.addEventListener("mouseleave", () => {
        box.setAttribute('class', 'history_box')
        input.setAttribute('class', 'left history_input')
        sidebar.setAttribute('class', 'right history_sidebar')
        opt.setAttribute('class', 'right history_sidebar none')
    })
}

function mouse_enter_opt_div(div) {
    div.addEventListener("mouseenter", () => {
        div.setAttribute('class', 'opt_div center agate_gray')
    })
}

function mouse_leave_opt_div(div) {
    div.addEventListener("mouseleave", () => {
        div.setAttribute('class', 'opt_div center')
    })
}

// 用于在点击图标的div的时候，获取到这个box的msg_id，从而执行接下来的操作
function get_msg_id_by_img_div(div) {
    let box_div = div.parentNode.parentNode
    return box_div.id.substring(3)

}


function fetch_del(div) {
    div.addEventListener("click", (e) => {
        // 阻止事件冒泡
        e.stopPropagation()
        // 获取msg_id
        const msg_id = get_msg_id_by_img_div(div)
        // fetch
        fetch('/gpt/del/' + msg_id)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                recursive_remove_div_by_id("history")
                load_history()
            })
    })
}

function fetch_modify(div) {
    div.addEventListener("click", (e) => {
        // 阻止事件冒泡
        e.stopPropagation()
        // 获取msg_id
        const msg_id = get_msg_id_by_img_div(div)
        // fetch
        fetch('/gpt/mod/' + msg_id)
            .then(response => response.json())
            .then(data => {
                console.log(data)
            })
    })
}

function fetch_more(div) {
    div.addEventListener("click", (e) => {
        // 阻止事件冒泡
        e.stopPropagation()
        // 获取msg_id
        const msg_id = get_msg_id_by_img_div(div)
        // fetch
        fetch('/gpt/more/' + msg_id)
            .then(response => response.json())
            .then(data => {
                console.log(data)
            })
    })
}

function recursive_remove_div_by_id(id) {
    console.log("remove past conversation...")
    let div = document.getElementById(id);
    while (div.hasChildNodes()) {
        div.removeChild(div.firstChild);
    }
}

function add_events() {
    let box_arr = document.getElementsByClassName('history_box')
    for (let i = 0; i < box_arr.length; i++) {
        let box_ = box_arr[i]
        let box_children = box_.children
        let input_ = box_children[0]
        let sidebar_ = box_children[1]
        let opt_ = box_children[2]
        let del_ = opt_.children[0]
        let mod_ = opt_.children[1]
        let more_ = opt_.children[2]
        mouse_enter(box_, input_, sidebar_, opt_)
        mouse_leave(box_, input_, sidebar_, opt_)
        mouse_enter_opt_div(del_)
        mouse_enter_opt_div(mod_)
        mouse_enter_opt_div(more_)
        mouse_leave_opt_div(del_)
        mouse_leave_opt_div(mod_)
        mouse_leave_opt_div(more_)
        fetch_del(del_)
        fetch_modify(mod_)
        fetch_more(more_)
    }
}

function create_history_list() {

    for (let i = 0; i < history_arr.length; i++) {
        let history = history_arr[i]
        let history_box = create_history_box(history[0], history[1], history[2])
        access_history(history_box)
    }
    add_events()
}
function loadAnswerText(answer_div, text) {
    // innerText的回车是\n, innerHTML的回车是<br>
    // answer_div.innerText = answer_div.innerText + text
    answer_div.innerText = answer_div.innerText + text
}

function load_history_div(content_list) {
    console.log("history div loading...")
    content_list.forEach(content => {
        console.log(content)
        if (content[2] === 3) {
            //  创建div：回答
            let answer_div = addAnswerDiv()
            loadAnswerText(answer_div, content[3])
            // 绑定点击事件，用于tts
            text_to_speach(answer_div)
            // 绑定事件，修改样式
            addConversationEvents(answer_div, 0)
        } else {
            // 创建div：提问
            let question_div = addQuestionDiv(content[3])
            // 绑定点击事件，用于tts
            text_to_speach(question_div)
            // 绑定事件，修改样式
            addConversationEvents(question_div, 1)
        }
        addClearDiv()
    })
}

function fetch_content_by_msg_id(msg_id) {
    fetch('/gpt/content/' + msg_id)
        .then(response => response.json())
        .then(data => {
            session_id = data["session_id"]
            let content_list = data["content_list"]
            load_history_div(content_list)
        })

}

// 访问历史记录
function access_history(box) {
    box.onclick = () => {
        // 先删除chatInfo聊天框内原有的所有聊天
        recursive_remove_div_by_id("chatInfo")
        console.log("click box...")
        // message位于数据库的索引
        const id = box.id.substring(3)
        // id -> session_id -> content[]
        fetch_content_by_msg_id(id)

    }

}

async function fetch_load_history() {
    await fetch('/gpt/loadHistory')
        .then(response => response.json())
        .then(data => {
            history_arr = data
        })
}

function create_history_div() {
    let container = document.getElementById('container')
    let history_div = document.createElement('div')
    history_div.setAttribute('id', 'history')
    history_div.setAttribute('class', 'right')
    container.appendChild(history_div)
}

async function load_history() {
    create_history_div()
    await fetch_load_history()
    create_history_list()
}


