(import [os [listdir]])
(import [datetime [datetime]])

;; this script emits HTML on standard out that constitutes a user
;; list. It denotes who has not updated their page from the
;; default. It also reports the time this script was run.

(def timestamp (.strftime (.now datetime) "%Y-%m-%d %H:%M:%S"))

(defn slurp [filename]
  (.read (open filename "r")))

(def default-html (slurp "/etc/skel/public_html/index.html"))

(defn dir->html [username]
  (let [[default (= default-html (slurp (.format "/home/{}/public_html/index.html" dirname)))]]
    (.format "<li><a href=\"http://tilde.town/~{}\">{}</a> {}</li>"
             username username
             (if default
               "(default :3)"
               ""))))

(def user-list (->> (listdir "/home")
                sorted
                (filter (fn [f] (not (= f "ubuntu"))))
                (map dir->html)
                (.join "\n")))

(print (.format "<sub>generated at {}</sub><br>{}" timestamp user-list))
