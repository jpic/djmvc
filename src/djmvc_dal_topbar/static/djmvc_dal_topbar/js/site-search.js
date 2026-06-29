document.addEventListener('autocompleteChoiceSelected', (event) => {
  const root = event.target.closest('.djmvc-site-search')
  if (!root) return
  const url = event.detail.choice.getAttribute('data-url')
  if (url) up.visit(url)
})