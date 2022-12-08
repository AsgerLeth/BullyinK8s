//////////////////////////////////////////////////////////////////
//
// Fortune Cookie Generator
//
//////////////////////////////////////////
    // TODO: Select a new (random) fortune cookie saying from the data stored in the
    // `fortunesList` variable. (HINT: You will use `Math.floor()` and
    // `Math.random()` to accomplish this.) Use this data to update the
    // `innerText` of the `#fortune-cookie-text` element.
    var fortunesList = [
        "”Today it's up to you to create the peacefulness you long for.”",
        "”A friend asks only for your time not your money.”",
        "”If you refuse to accept anything but the best, you very often get it.”",
        "”A smile is your passport into the hearts of others.”",
        "”A good way to keep healthy is to eat more Chinese food.”",
        "”Your high-minded principles spell success.”",
        "”Hard work pays off in the future, laziness pays off now.”",
        "”Change can hurt, but it leads a path to something better.”",
        "”Enjoy the good luck a companion brings you.”",
        "”People are naturally attracted to you.”",
        "”Hidden in a valley beside an open stream- This will be the type of place where you will find your dream.”",
        "”A chance meeting opens new doors to success and friendship.”",
        "”You learn from your mistakes... You will learn a lot today.”",
        "”If you have something good in your life, don't let it go!”",
        "”What ever you're goal is in life, embrace it visualize it, and for it will be yours.”",
        "”Your shoes will make you happy today.”",
        "”You cannot love life until you live the life you love.”",
        "”Be on the lookout for coming events; They cast their shadows beforehand.”",
        "”Land is always on the mind of a flying bird.”",
        "”The man or woman you desire feels the same about you.”",
        "”Meeting adversity well is the source of your strength.”",
        "”A dream you have will come true.”",
        "”Our deeds determine us, as much as we determine our deeds.”",
        "”Never give up. You're not a failure if you don’t give up.”",
        "”You will become great if you believe in yourself.”",
        "”There is no greater pleasure than seeing your loved ones prosper.”",
        "”You will marry your lover.”",
        "”A very attractive person has a message for you.”",
        "”You already know the answer to the questions lingering inside your head.”",
        "”It is now, and in this world, that we must live.”",
        "”You must try, or hate yourself for not trying.”",
        "”You can make your own happiness.”"
    ];
    
    var generateFortuneCookie = function() {
        // This is where your code for the Fortune Cookie generator goes.
        // You will use the fortunesList variable defined lower in this file
        // to supply your fortune cookies with text.
        
    
        // TODO: Grab the paragraph with the ID
        // `fortune-cookie-text` to be able to insert text into that element.
       
        
        // TODO: Update the Previous Fortunes list with the current `innerHTML`
        // value of `#fortune-cookie-text`. Follow these steps:
            // 1. Create a new `li` element with the `document.createElement()` method.
                    //empty li
           var fortuneElement = document.createElement("li"); 
            // 2. Set the `innerHTML` of that element equal to the `innerHTML` of
            //    the `#fortune-cookie-text` element.
                    //adds test to p
                    var fortuneCookieText=document.getElementById('fortune-cookie-text');
                    //sets the empty li to the content of the p
                    fortuneElement.innerHTML=fortuneCookieText.innerHTML;
                      // 3. Select the `#previous-fortunes-container` container and use
            //    `appendChild()` to append the new `li` element you created above.
                    var usedFortunes = document.getElementById("previous-fortunes-container");
                            usedFortunes.appendChild(fortuneElement);
      
            // 4. You should see the previous fortune cookie saying show up in the list.
                //selectes a random fortune
        
        // TODO: Select a new (random) fortune cookie saying from the data stored in the
        // `fortunesList` variable. (HINT: You will use `Math.floor()` and
        // `Math.random()` to accomplish this.) Use this data to update the
        // `innerText` of the `#fortune-cookie-text` element.
    
                fortuneCookieText.innerText=fortunesList[Math.floor(Math.random() * fortunesList.length)];
    }
    
    
    // The following data list is provided for you to use in your code.
    
    