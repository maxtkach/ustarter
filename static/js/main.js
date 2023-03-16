const container = document.querySelector('.recent__projects');
let isDown = false;
let startX;
let scrollLeft;

container.addEventListener('mousedown', (e) => {
  isDown = true;
  startX = e.pageX - container.offsetLeft;
  scrollLeft = container.scrollLeft;
});

container.addEventListener('mouseleave', () => {
  isDown = false;
});

container.addEventListener('mouseup', () => {
  isDown = false;
});

container.addEventListener('mousemove', (e) => {
  if (!isDown) return;
  e.preventDefault();
  const x = e.pageX - container.offsetLeft;
  const walk = (x - startX) * 3;
  container.scrollLeft = scrollLeft - walk;
});

const container2 = document.querySelector('.popular__projects');
let isDown2 = false;
let startX2;
let scrollLeft2;

container2.addEventListener('mousedown', (e) => {
  isDown2 = true;
  startX2 = e.pageX - container2.offsetLeft;
  scrollLeft2 = container2.scrollLeft;
});

container2.addEventListener('mouseleave', () => {
  isDown2 = false;
});

container2.addEventListener('mouseup', () => {
  isDown2 = false;
});

container2.addEventListener('mousemove', (e) => {
  if (!isDown2) return;
  e.preventDefault();
  const x = e.pageX - container2.offsetLeft;
  const walk = (x - startX2) * 3;
  container2.scrollLeft = scrollLeft2 - walk;
});

