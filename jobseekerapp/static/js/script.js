
    let counters = document.querySelectorAll(".count");

    counters.forEach(counter => {

        let target = Number(counter.dataset.count);
        let current = 0;

        let timer = setInterval(() => {

            current++;

            counter.innerText = current;

            if (current >= target) {
                clearInterval(timer);
                counter.innerText = target;
            }

        }, 100);

    });
