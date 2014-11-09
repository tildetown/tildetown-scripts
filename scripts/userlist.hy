(import [os [listdir]])
(import [os.path [getmtime]])
(import [datetime [datetime]])

;; this script emits HTML on standard out that constitutes a user
;; list. It denotes who has not updated their page from the
;; default. It also reports the time this script was run.

(def timestamp (.strftime (.now datetime) "%Y-%m-%d %H:%M:%S"))

(defn slurp [filename]
  (try
    (.read (apply open [filename "r"] {"encoding" "utf-8"}))
  (catch [e Exception]
    "")))

(def default-html (slurp "/etc/skel/public_html/index.html"))

(defn dir->html [username]
  (let [[default (= default-html (slurp (.format "/home/{}/public_html/index.html" username)))]]
    (.format "<li><a href=\"http://tilde.town/~{}\">{}</a> {}</li>"
             username username
             (if default
               "(default :3)"
               ""))))

(defn modify-time [username]
  (getmtime (.format "/home/{}/public_html" username)))


(defn sort-user-list [usernames]
  (apply sorted [usernames] {"key" modify-time}))

(defn user-generator [] (->> (listdir "/home")
                             (filter (fn [f] (and (not (= f "ubuntu")) (not (= f "poetry")))))))

(def user-list (->> (user-generator)
                    sort-user-list
                    reversed
                    (map dir->html)
                    (.join "\n")))

(print (.format "our esteemed users ({})<br> <sub>generated at {}</sub><br><ul>{}</ul>"
                (len (user-generator))
                timestamp
                user-list))
