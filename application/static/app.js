const span = document.querySelector('.copy_span')

const texts = ['Businesses', 'Partners', 'Customers', 'Clients', 'Leads']

let inText = 0

setInterval(() => {
    inText++
    if (inText == texts.length){
        inText = 0
    }
    span.innerHTML = texts[inText]
}, 4000)
