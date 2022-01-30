mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"email@domain\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]
base='dark'
primaryColor='#7792E3'
" > ~/.streamlit/config.toml

echo "\
" > ~/.streamlit/secrets.toml