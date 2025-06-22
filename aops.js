let clickedTimes = 0;

let pagename = "1954 AHSME Problems/Problem 47";

async function addAnswer2(pagename) {
  let answersTitle = `${pagename?.split(" Problems/Problem")[0]} Answer Key`;
  let apiEndpoint = "https://artofproblemsolving.com/wiki/api.php";
  let params = `action=parse&page=${answersTitle}&format=json`;

  let response = await fetch(`${apiEndpoint}?${params}&origin=*`);
  let json = await response.json();
  let answerText = json.parse?.text["*"];
  console.log(answerText);

}

async function addAnswer(pagename) {
  clickedTimes++;
  answerTimes++;
  let clickedTimesThen = clickedTimes;
  answerTries = 0;
  progressUpdated = false;
  let answersTitle = `${pagename?.split(" Problems/Problem")[0]} Answer Key`;
  let apiEndpoint = "https://artofproblemsolving.com/wiki/api.php";
  let params = `action=parse&page=${answersTitle}&format=json`;

  let response = await fetch(`${apiEndpoint}?${params}&origin=*`);
  let json = await response.json();
  let answerText = json.parse?.text["*"];
  let problemNum = computeNumber(pagename);
  let answer = $($.parseHTML(answerText))
    ?.find("ol li")
    ?.eq(problemNum - 1)
    ?.text();
  if (answer) {
    if (clickedTimes === clickedTimesThen) {
      $("#problem-text").after(`<div class="answer-check">
      <form class="options-input answer-options" onsubmit="return false">
        <input class="input-field" id="input-answer"
          type="text" placeholder="Enter answer (optional)"/>
        <button type="submit" class="input-button" id="answer-button">
          Check Answer
        </button>
      </form>
      <div class="answer-feedback"></div>
    </div>`);

      $("#answer-button").click(async function () {
        let originalAnswer = sanitize($("#input-answer").val());
        originalAnswer = originalAnswer.toUpperCase();
        let finalAnswer = originalAnswer;
        if (finalAnswer) {
          if (computeTest(pagename) === "AIME")
            finalAnswer = originalAnswer.padStart(3, "0");
          answerTries++;

          if (answerTries == 1) {
            localStorage.setItem(
              "numToday",
              JSON.parse(localStorage.getItem("numToday")) + 1
            );
            localStorage.setItem(
              "numAnswered",
              JSON.parse(localStorage.getItem("numAnswered")) + 1
            );
          }
          if (
            finalAnswer === answer ||
            (pagename === "2012 AMC 12B Problems/Problem 12" &&
              (finalAnswer === "D" || finalAnswer === "E")) ||
            (pagename === "2015 AMC 10A Problems/Problem 20" &&
              finalAnswer === "B") ||
            (pagename === "2022 AIME II Problems/Problem 8" &&
              (finalAnswer === "080" || finalAnswer === "081"))
          ) {
            $("#input-answer").removeClass("glow");
            void document.getElementById("input-answer").offsetWidth;
            $("#input-answer").addClass("glow");

            $(".answer-feedback")
              .prepend(`<div class="feedback-item correct-feedback">
                ${originalAnswer} is correct! :)
              </div>`);
            if (!progressUpdated) {
              $(".progress-hidden").removeClass("progress-hidden");
              progressUpdated = true;
              if (answerTries == 1) {
                streakCount++;
                if (
                  streakCount > JSON.parse(localStorage.getItem("numStreak"))
                )
                  localStorage.setItem("numStreak", streakCount);

                $(".streak-bar").removeClass("bar-hidden");
                $(".question-bar.right-questions").removeClass("bar-hidden");
                $(".question-bar.right-questions").css(
                  "flex-grow",
                  parseInt(
                    $(".question-bar.right-questions").css("flex-grow")
                  ) + 1
                );
                $("#right-num").text(
                  parseInt(
                    $(".question-bar.right-questions").css("flex-grow")
                  )
                );
                localStorage.setItem(
                  "numCorrect",
                  JSON.parse(localStorage.getItem("numCorrect")) + 1
                );
              } else {
                $(".streak-bar").removeClass("bar-hidden");
                $(".question-bar.retry-questions").removeClass("bar-hidden");
                $(".question-bar.retry-questions").css(
                  "flex-grow",
                  parseInt(
                    $(".question-bar.retry-questions").css("flex-grow")
                  ) + 1
                );
                $("#retry-num").text(
                  parseInt(
                    $(".question-bar.retry-questions").css("flex-grow")
                  )
                );
                localStorage.setItem(
                  "numRetry",
                  JSON.parse(localStorage.getItem("numRetry")) + 1
                );
              }
              $("#solutions-header").click();
            }
          } else {
            streakCount = 0;

            $("#input-answer").removeClass("shake");
            void document.getElementById("input-answer").offsetWidth;
            $("#input-answer").addClass("shake");

            $(".answer-feedback")
              .prepend(`<div class="feedback-item wrong-feedback">
            ${originalAnswer} is wrong :(
            </div>`);
          }
        }
        $("#input-answer").val("");
        $("#streak-num").text(streakCount);
      });
    }
  }
}