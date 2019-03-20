(function () {
    let categories_url = 'http://127.0.0.1:8000/api/categories/'
    let scrape_url = 'http://127.0.0.1:8000/api/scrape/create/'
    let base_books = 'http://127.0.0.1:8000/api/books/'
    let books_url = base_books + '?category='


    //Scrape button
    $('#button_scrape')
        .click((e) => {
            e.preventDefault()
            $.ajax({
                method: 'POST',
                url: scrape_url,
                success: function (result) {
                    console.log(result);
                    alert("Scrape complete")
                },
                error: (err) => {
                    console.log(err);
                    alert("Something went wrong")
                }
            })
        })


    // Categories list
    $.ajax({
        method: 'GET',
        url: categories_url,
        dataType: 'JSON',
        success: function (data) {
            categories_string = ""
            data.forEach((value) => {
                categories_string += `<li class="list-group-item">
                <a class="viewDetail" data-id="${value.id}">${value.name}</a></li>`
            });

            content = `<ul class="list-group" id="categories_list">${categories_string}</ul>`

            $('#categories').append(content);

            $('.viewDetail').each((i, elm) => {
                $(elm).on('click', (e) => {
                    booksViewList($(elm));
                });
            });
        },
        error: (err) => {
            return err
        }
    });


    // Books table
    function booksViewList(el) {
        
        let rows = '';

        //get category id
        category_id = $(el).data('id');
        
        return $.ajax({

            method: 'GET',
            url: books_url + category_id,
            dataType: 'JSON',
            success: function (data) {

                $('#myTable > tbody').empty();

                results = data;     

                results.forEach( (result) => {

                    rows += `
                        <tr>
                            <td><img src="${result.thumbnail_url}"></td>
                            <td>${result.upc}</td>
                            <td>${result.title}</td>
                            <td>${result.price}</td>
                            <td>${result.stock}</td>
                            <td class="">${(result.product_description).substring(1,90)+'...'}</td>
                            <td><button data-id="${result.id}" class="btn btn-danger deleteBtn">Delete</button></td>
                        </tr>
                    `
                });

                $('#myTable > tbody').append(rows);
                $('.deleteBtn').each((i ,elm) => {
                    $(elm).on('click', (e) => {
                        deleteBtnAction($(elm));
                    });
                });
            }
        });
    }


    // Delete book by id
    function deleteBtnAction(el){
        book_id = $(el).data('id');

        return $.ajax({
            method: 'DELETE',
            url: base_books + book_id,
            dataType: 'JSON',
            success: function (data) {
                $(el).parents()[1].remove()
                alert("Book successfully removed")
            },
            error: function (err) {
                console.log(err)
                alert("Error")
            }
        })
    }
    

    // JQuery generic filter
    $("#filterTable").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

})();
