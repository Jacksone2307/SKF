function save_track(title, url, key) {

    entry = {
        title: title,
        url: url,
        key: key
    }
    console.log(entry);
    fetch("{{url_for('home_bp.save_track')}}", {
        method: 'POST',
        credentials: 'include',
        headers: {
            "content-type": "application/json"
        },
        body: JSON.stringify(entry),
        cache: 'no-cache'
    })
}