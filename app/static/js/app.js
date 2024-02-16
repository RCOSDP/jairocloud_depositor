import React, { useState, useRef, createContext, useContext } from 'react';
import { createRoot } from 'react-dom/client';
// import { DatePicker } from 'react-datepicker';

const contentFilesContext = createContext([]);
const setContentFilesContext = createContext(null);
const thumbnailContext = createContext([]);
const setThumbnailContext = createContext(null);

const FileProvider = ({ children }) => {
    const [contentfiles, setcontentfiles] = useState([]);
    const [thumbnail, setthumbnail] = useState([]);

    return (
        <contentFilesContext.Provider value={contentfiles}>
            <setContentFilesContext.Provider value={setcontentfiles}>
                <thumbnailContext.Provider value={thumbnail}>
                    <setThumbnailContext.Provider value={setthumbnail}>
                        {children}
                    </setThumbnailContext.Provider>
                </thumbnailContext.Provider>
            </setContentFilesContext.Provider>
        </contentFilesContext.Provider>
    )
}

const useFilesValue = () => useContext(contentFilesContext);
const useFilesSetValue = () => useContext(setContentFilesContext);
const useThumbnailValue = () => useContext(thumbnailContext);
const useThumbnailSetValue = () => useContext(setThumbnailContext);

function PDFform() {
    const contentfiles = useFilesValue();
    const setcontentfiles = useFilesSetValue();
    const [pdffile, setpdffile] =useState([]); 
    const contentfilenames = contentfiles.map(contentfile => contentfile.name);
    function addfiles(files) {
        // 一時的なリストをdeepcopyで生成
        let tmpfiles = contentfiles.map(contentfile => contentfile)
        // リストに名前が存在しないなら一時リストにプッシュ
        if (files.length > 0) {
            const firstFile = files[0];
            if(check_filesize_over_100MB(firstFile)){
                console.log("ファイルサイズが100MBを超えています。")
                console.log(firstFile.name)
            } else if (firstFile.type === "application/pdf") {
                if (!(contentfilenames.includes(firstFile.name))) {
                    tmpfiles.push(firstFile)
                }
                if (pdffile.length===0 || pdffile[0].name!==firstFile.name){
                    setpdffile([firstFile])
                }
            } else {
                console.log("PDFファイルではありません。")
            }
        } else {
            console.log("ドロップされたファイルはありません");
        }
        setcontentfiles(tmpfiles);
    }
    
    function deletefile(filename) {
        setpdffile([]);
    }
    return (
        <div className="row row-4">
            <div className="col-sm-12">
                <p className="text-center">pdf自動入力フォーム</p>
                <div className="files-upload-zone">
                    <DropFileArea addfiles={addfiles} />
                    <p className="text-center legend"><strong>— OR —</strong></p>
                    <AddFileButton addfiles={addfiles} acceptfiletype={"application/pdf"} />
                </div>
                <p className="text-center">登録可能なファイルは「pdf」のみ</p>
                <p className="text-center">
                    <button className="btn btn-success">
                        <span className="glyphicon glyphicon-plus"></span>&nbsp;
                        PDFからメタデータの自動入力
                    </button>
                </p>
            {(pdffile.length !== 0) && <Datalist contentfiles={pdffile} deletefile={deletefile} />}
            </div>
        </div>

    )
}

function Datalistform({ order, value, item }) {
    return (
        <Textform metadatatitle={("title_i18n" in item) && ("ja" in item.title_i18n) ? item.title_i18n.ja : item.title} value={""} order={order} item={item} />
    )
}

function Datalist({ contentfiles, deletefile }) {
    return (
        <div className="panel panel-default">
            <div className="panel-heading">
                <div className="row">
                    <div className="col-sm-6">
                    </div>
                </div>
            </div>
            <table className="table">
                <tbody><tr>
                    <th>Filename</th>
                    <th>Size</th>
                    <th className="text-center">Actions</th>
                </tr>
                    {contentfiles.map(file => (
                        (<tr key={file.name}>
                            <td>{file.name}</td>
                            <td>{Math.round(file.size / 1024)}KB</td>
                            <td className="text-center">
                                <a onClick={() => deletefile(file.name)}>
                                    削除
                                </a>
                            </td>
                        </tr>)
                    ))}
                </tbody></table>
            <div className="panel-footer"></div>
        </div>
    )
}

function DropFileArea({ addfiles }) {

    function dragOverHandler(event) {
        event.preventDefault()
    }

    function dropFile(event) {
        event.preventDefault();
        let isfiles = true;
        if (event.dataTransfer.files) {
            [...event.dataTransfer.items].forEach((item) => {
                // ドロップしたものがファイルでない場合は拒否する
                if (item.kind !== "file") {
                    console.log("not file");
                    isfiles = false;
                }
            })
        } else {
            console.log("no files");
            isfiles = false;
        }
        if (isfiles == true) {
            addfiles(event.dataTransfer.files)
        }
    }

    return (
        <div className="well" onDragOver={(e) => { dragOverHandler(e) }} onDrop={(e) => { dropFile(e) }}>
            <center>
                Drop files or folders here
            </center>
        </div>)
}

function AddFileButton({ addfiles, acceptfiletype }) {
    const self = useRef();
    function fileaddaction() {
        self.current.click();
    }
    return (
        <p className="text-center">
            <button className="btn btn-primary" onClick={fileaddaction} >
                Click to select
            </button>
            <input ref={self} type="file" className="hidden" multiple accept={acceptfiletype} onChange={(e) => { addfiles(e.target.files); e.target.value = ""; }} />
        </p>
    )
}

function FileUploadForm({ }) {
    const contentfiles = useFilesValue();
    const setcontentfiles = useFilesSetValue();
    const contentfilenames = contentfiles.map(contentfile => contentfile.name);
    function addfiles(files) {
        // 一時的なリストをdeepcopyで生成
        let tmpfiles = contentfiles.map(contentfile => contentfile)
        // リストに名前が存在しないなら一時リストにプッシュ
        Array.from(files).forEach(file => {
            if(check_filesize_over_100MB(file)){
                console.log("ファイルサイズが100MBを超えています。")
                console.log(file.name)
            }else if (!(contentfilenames.includes(file.name))) {
                contentfilenames.push(file.name)
                tmpfiles.push(file)
            }
        })
        // 一時的なリストからレンダー
        setcontentfiles(tmpfiles);
    }
    function deletefile(filename) {
        let tmpfiles = contentfiles.map(contentfile => contentfile).filter(file => file.name !== filename)
        setcontentfiles(tmpfiles);
    }

    return (
        <div className="row row-4 list-group-item">
            <div className="col-sm-12">
                <div className="files-upload-zone">
                    <DropFileArea addfiles={addfiles} />
                    <p className="text-center legend"><strong>— OR —</strong></p>
                    <AddFileButton addfiles={addfiles} />
                </div>
                {(contentfiles.length !== 0) && <Datalist contentfiles={contentfiles} deletefile={deletefile} />}
            </div>
        </div>

    )
}

function ThumbnailUploadForm() {
    const thumbnail = useThumbnailValue();
    const setthumbnail = useThumbnailSetValue();
    const files = useFilesValue();
    console.log(files)
    function addfiles(files) {
        if (files.length > 0) {
            const firstFile = files[0];
            if(check_filesize_over_100MB(firstFile)){
                console.log("ファイルサイズが100MBを超えています。")
            }else if(!(firstFile.type.startsWith('image/'))) {
                console.log("画像ファイルではありません。")
            } else {
                setthumbnail([firstFile]);
            }
        } else {
            console.log("ドロップされたファイルはありません");
        }
    }
    function deletefile(filename) {
        setthumbnail([]);
    }

    return (
        <div className="row row-4 list-group-item">
            <div className="col-sm-12">
                <div className="files-upload-zone">
                    <DropFileArea addfiles={addfiles} />
                    <p className="text-center legend"><strong>— OR —</strong></p>
                    <AddFileButton addfiles={addfiles} acceptfiletype={"image/*"} />
                </div>
                <p className="text-center">登録可能なファイルは「gif, jpg, jpe, jpeg, png, bmp」</p>
                {(thumbnail.length !== 0) && <Datalist contentfiles={thumbnail} deletefile={deletefile} />}
            </div>
        </div>

    )
}

function Metadatatitle({ title, metadatakey }) {
    let required = false;
    let classvalue;
    if (schema.required.includes(metadatakey)) {
        required = true;
    }
    if (required) {
        classvalue = "col-sm-3 control-label field-required";
    } else {
        classvalue = "col-sm-3 control-label";
    }
    return (
        <label className={classvalue}>
            {title}
        </label>
    )
}

function Textform({ metadatatitle, value, order, item }) {
    let readonly = false;
    // とりあえず今はコメントアウト
    // if ("readonly" in item && item.readonly == true) {
    //     readonly = true;
    // }
    return (
        <div className="form-group schema-form-text">
            <Metadatatitle title={metadatatitle} metadatakey={item.key} />
            <div className="col-sm-9">
                <input type="text"
                    className="form-control input-form"
                    id={item.key.replaceAll("[]", "[" + String(order) + "]")}
                    name={item.key.split(".")[item.key.split(".").length - 1]}
                    schema-validate="form"
                    defaultValue={value}
                    disabled={readonly}
                ></input>
            </div>
        </div>
    );
}

function Textareaform({ metadatatitle, value, order, item }) {
    return (
        <div className="form-group schema-form-textarea">
            <Metadatatitle title={metadatatitle} metadatakey={item.key} />
            <div className="col-sm-9">
                <textarea className="form-control input-form"
                    id={item.key.replaceAll("[]", "[" + String(order) + "]")}
                    name={item.key.split(".")[item.key.split(".").length - 1]}
                    schema-validate="form"
                    defaultValue={value}></textarea>
            </div>
        </div>
    );
}


function Selectform({ metadatatitle, map, order, value, item }) {
    const titlemap = [];
    map.forEach(element => {
        titlemap.push(
            <option label={element.name} value={element.value} key={item.key.replaceAll("[]", "[" + String(order) + "]") + element.value}></option>
        );
    })
    return (
        <div className="form-group schema-form-select">
            <Metadatatitle title={metadatatitle} metadatakey={item.key} />
            <div className="col-sm-9">
                <select className="form-control input-form" schema-validate="form" id={item.key.replaceAll("[]", "[" + String(order) + "]")} name={item.key.split(".")[item.key.split(".").length - 1]} defaultValue={value}>
                    <option value=""></option>
                    {titlemap}
                </select>
            </div>
        </div>

    )
}

// 未完成jpcoar2.0では使わない
function Radioform({ metadatatitle, map, order, value, item }) {
    const titlemap = [];
    map.forEach(element => {
        titlemap.push(
            <div className="radio">
                <label>
                    <input type="radio"
                        id={item.key.replaceAll("[]", "[" + String(order) + "]")}
                        name={item.key.replaceAll("[]", "[" + String(order) + "]")}
                        value={element.value} />
                    <span ng-bind-html="item.name">{element.name_i18n.ja}</span>
                </label>
            </div >
        );
    })

    return (
        <div className="form-group schema-form-radios">
            <Metadatatitle title={metadatatitle} metadatakey={item.key} />
            <div className="col-sm-9">
                {titlemap}
            </div>
        </div>
    )
}


// 実装できていない。いまはとりあえず　input text型である。
function Datepickerform({ order, value, item }) {
    // const [selectedDate, setSelectedDate] = useState<Date>();
    let metadatatitle = ("title_i18n" in item) && ("ja" in item.title_i18n) ? item.title_i18n.ja : item.title;
    return (
        <div className="form-group schema-form-datepicker">
            <Metadatatitle title={metadatatitle} metadatakey={item.key} />

            <div className="col-sm-9">
                <input type="data"
                    className="form-control input-form"
                    id={item.key.replaceAll("[]", "[" + String(order) + "]")}
                    name={item.key.split(".")[item.key.split(".").length - 1]}
                    schema-validate="form"
                    defaultValue={value}
                ></input>
            </div>
            {/* <DatePicker
                                dateFormat="yyyy-MM-dd"
                                locale="ja"
                                selected={selectedDate}
                                showTimeSelect
                                timeIntervals={30} /> */}
        </div>
    )
}


// 未完成jpcoar2.0では使わない
function Checkboxesform({ order, value, item }) {
    const titlemap = [];
    let metadatatitle = ("title_i18n" in item) && ("ja" in item.title_i18n) ? item.title_i18n.ja : item.title
    map = item.titleMap
    map.forEach(element => {
        titlemap.push(
            <label className="checkbox col-sm-4 checkbox-input">
                <input type="checkbox" className="touched" schema-vaidate="form" />
                <span style="overflow-wrap: break-word;">{element.name}</span>
            </label>
        );
    })
    return (
        <div className="form-group schema-form-select">
            <Metadatatitle title={metadatatitle} metadatakey={item.key} />
            <div className="col-sm-9">
                <div className="checkbox">
                    <select sf-changed="form" className="form-control" schema-validate="form" id={item.key.replaceAll("[]", "[" + String(order) + "]")} defaultValue={value}>
                        <option className value=""></option>
                        {titlemap}
                    </select>
                </div>
            </div>
        </div>
    )
}

function HTMLpicker({ html }) {

    return (<div>{html}</div>);
}

function Inputlist({ form, count }) {
    const input_field = [];
    if (!("items" in form)) {
        input_field.push(<Datepickerform order={count} item={form} key={form.key} />);
    } else {
        form.items.forEach(item => {
            if ("type" in item) {
                if (item.type === "text") {
                    input_field.push(
                        <Textform metadatatitle={("title_i18n" in item) && ("ja" in item.title_i18n) ? item.title_i18n.ja : item.title} value={""} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "textarea") {
                    input_field.push(
                        <Textareaform metadatatitle={("title_i18n" in item) && ("ja" in item.title_i18n) ? item.title_i18n.ja : item.title} map={item.titleMap} value={""} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "select") {
                    input_field.push(
                        <Selectform metadatatitle={("title_i18n" in item) && ("ja" in item.title_i18n) ? item.title_i18n.ja : item.title} map={item.titleMap} value={""} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "radios") {
                    input_field.push(
                        <Radioform metadatatitle={("title_i18n" in item) && ("ja" in item.title_i18n) ? item.title_i18n.ja : item.title} map={item.titleMap} value={""} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "fieldset") {
                    input_field.push(<Panelform title={("title_i18n" in item) && ("ja" in item.title_i18n) ? item.title_i18n.ja : item.title} form={item} order={count} key={item.key} />);
                } else if (item.type === "contentfile" || item.type === "thumbnail") {
                    input_field.push(<Panelform form={item} key={item.key} />);
                } else if (item.type === "template") {
                    if ("templateUrl" in item) {
                        let template = item.templateUrl.split('/').pop()
                        if (template === "datepicker.html" || template === "datepicker_multi_format.html") {
                            input_field.push(<Datepickerform order={count} item={item} key={item.key} />);
                        } else if (template === "datalist.html") {
                            input_field.push(<Datalistform order={count} item={item} key={item.key} />);
                        } else if (template === "checkboxes.html") {
                            input_field.push(<Checkboxesform order={count} item={item} map={item.titleMap} key={item.key} />)
                        }
                    } else if ("template" in item) {
                        input_field.push(<div></div>);
                    }
                } else {
                    input_field.push(<div></div>);
                }

            } else {
                input_field.push(<Panelform form={item} key={item.key} />);
            }
        })
    };
    return (
        <div className="list-group">
            {input_field}
        </div>
    );
}

function Panelform({ form }) {
    const [count, setcount] = useState(0);
    const [inputlists, setInputlists] = useState([(<Inputlist form={form} count={count} key={form.key + "[" + String(count) + "]"} />)]);
    const [toggle, settoggle] = useState(" hidden");
    let isArray = false;

    function addarray() {
        setInputlists(prevComponents => [...prevComponents,
        (<Inputlist form={form} count={count + 1} key={form.key + "[" + String(count + 1) + "]"} />
        )]);
        setcount(count + 1);
    }

    function reducearray(key) {
        setInputlists(prevItems => prevItems.filter(inputlist => inputlist.key !== key));
    }

    function togglepanel() {
        if (toggle == " hidden") {
            settoggle("")
        } else {
            settoggle(" hidden")
        }
    }

    if (form.add == "New") {
        isArray = true;
    }


    return (
        <fieldset className="schema-form-fieldset flexbox" id={form.key} name={form.key.split(".")[form.key.split(".").length - 1]}>
            <div className="panel panel-default deposit-panel">
                <div className="panel-heading"><a className="panel-toggle" onClick={() => togglepanel()}>
                    {("title_i18n" in form) && ("ja" in form.title_i18n) ? form.title_i18n.ja : form.title}
                </a>
                </div>
                <div className={"panel-body panel-body2 list-group" + toggle}>
                    <div className="schema-form-array">
                        <div className="col-sm-12">
                            {(form.type == "contentfile") && <FileUploadForm />}
                            {(form.type == "thumbnail") && <ThumbnailUploadForm />}
                            {inputlists.map(inputlist => (
                                <li className="list-group-item ui-sortable" id={form.key + "[" + count + "]"} key={inputlist.key}>
                                    {isArray &&
                                        (<div className="close-container clear-form">
                                            <button type="button" className={"close pull-right"} onClick={() => reducearray(inputlist.key)}>
                                                <span aria-hidden="true">×</span>
                                            </button>
                                        </div>)}
                                    {inputlist}
                                </li>
                            ))}
                        </div>
                        {isArray &&
                            (<button onClick={() => addarray()} type="button" className={"btn btn-success pull-right"}>
                                <i className="glyphicon glyphicon-plus"></i>
                                New
                            </button>)}
                    </div>
                </div>
            </div>
        </fieldset >
    )
}


function SubmitButton() {
    const contentfiles = useFilesValue();
    const thumbnail = useThumbnailValue();
    const [disabled, setdisabled] = useState(false);
    // ファイルをBase64にエンコードする関数
    function encodeFileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = function (event) {
                const base64Data = event.target.result.split(",")[1];
                console.log(file.name+":"+base64Data.length)
                resolve({ "name": file.name, "base64": base64Data });
            };
            reader.onerror = function (error) {
                reject(error);
            };
            reader.readAsDataURL(file);
        });
    }

    // 複数のファイルをBase64にエンコードする関数
    function encodeFilesToBase64(files) {
        const promises = files.map(file => {
            return encodeFileToBase64(file)
        });
        return Promise.all(promises);
    }


    function request_python(metadata, files, thumb) {
        const dataforrequest = { "item_metadata": metadata, "contentfiles": files, "thumbnail": thumb }
        // const dataforrequest = { "item_metadata": metadata, "contentfiles": [], "thumbnail": thumb }
        console.log("request_python")
        console.log(dataforrequest)
        return fetch("/item_register/register", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(dataforrequest)
        })
    }

    function itemRegister() {
        console.log("aaaaaaaaa")
        let metadata = load_metadata()
        console.log(metadata)
        let files = [];
        let thumb = null;
        encodeFilesToBase64(contentfiles).then(base64files => {
                files = base64files.map(base64file => base64file) // 全てのファイルのBase64データの配列が表示される
                console.log("nnnnn")
                console.log(files)
                return encodeFilesToBase64(thumbnail)
            }).then(thumbnail => {
                console.log("thumb")
                thumb = thumbnail.map(base64thumbnail => base64thumbnail)
                return request_python(metadata, files, thumb)
            }).catch(error => {
                console.error('Error encoding files:', error);
            }).finally(
                console.log("finally")
            );
        

    }
    return (
        <div className="col-sm-12">
            <div className="col-sm-offset-3 col-sm-6">
                <div className="list-inline text-center">
                    
                    <button id="submit_button" className="btn btn-info next-button" disabled={disabled} onClick={itemRegister}>
                        送信
                    </button>
                </div>
            </div>
        </div>)
}



function ItemRegisterPanel({ forms, schema }) {
    let count = 0;
    const input_forms = [];
    forms.forEach(form => {
        if (!("system_prop" in schema.properties[form.key] && schema.properties[form.key].system_prop == true)) {
            input_forms.push(
                <div className="form_metadata_property" key={form.key}>
                    <Panelform form={form} />
                </div>
            )
            count++;
        }
    });
    return (
        <FileProvider>
            <PDFform />
            <hr />
            <div className="form">
                {input_forms}
            </div>
            <SubmitButton />
        </FileProvider>
    )
}

function load_panel(panel, property, nest) {
    panel.querySelectorAll('.schema-form-fieldset').forEach(function (element) {
        if (element.id.split(".").length == nest) {
            property[element.name] = []
            let propers = property[element.name]
            element.querySelectorAll('li.list-group-item.ui-sortable').forEach(function (elem) {
                if (elem.id.split(".").length == nest) {
                    let proper = {}
                    elem.querySelectorAll('.input-form.form-control').forEach(function (e) {
                        if (e.id.split('.').length <= nest + 1) {
                            if (e.value != "")
                                proper[e.name] = e.value;
                        }
                    })
                    if (elem.querySelector('li.list-group-item.ui-sortable') != null) {
                        load_panel(elem, proper, nest + 1)
                    }
                    if (Object.keys(proper).length) {
                        propers.push(proper)
                    }
                }
            })
            // 入力がない項目のキーを削除
            if (!(propers.length)) {
                delete property[element.name];
            }
        }
    })
}

function load_metadata() {
    let item_metadata = {}
    // 項目ごとにHTMLを取得
    document.querySelectorAll('.form_metadata_property').forEach(function (element) {

        //項目の大枠を取得
        let metadata_property = element.querySelector('.schema-form-fieldset');

        // item_metadataに項目のキーを追加し、操作できるようにする。
        item_metadata[metadata_property.name] = []

        let properties = item_metadata[metadata_property.name]

        metadata_property.querySelectorAll('li.list-group-item.ui-sortable').forEach(function (elemen) {
            if (elemen.id.split(".").length == 1) {
                let property = {}
                //
                elemen.querySelectorAll('.input-form.form-control').forEach(function (e) {
                    if (e.id.split('.').length <= 2) {
                        if (e.value != "") {
                            property[e.name] = e.value;
                        }
                    }
                })

                load_panel(elemen, property, 2)
                if (Object.keys(property).length) {
                    properties.push(property)
                }
            }
        })
        // 入力がない項目のキーを削除
        if (!(properties.length)) {
            delete item_metadata[metadata_property.name];
        }
    })

    return item_metadata
}

function check_filesize_over_100MB(file){
    /// ファイルサイズ取得
    const fileSize = file.size;
    /// MB単位のファイルサイズ計算
    const fileMib = fileSize/1024**2;
    if (fileMib < 100){
        return false
    }else{
        return true
    }
}

/**
 * Custom bs-datepicker.
 * Default bs-datepicker: just support one pattern for input.
 * Custom bs-datepicker: support validate three pattern.
 * Used way:
 *  templateUrl: /static/templates/weko_deposit/datepicker_multi_format.html
 *  customFormat: enter your pattern.
 *    if it none, pattern are yyyy-MM-dd, yyyy-MM, yyyy.
*/
let Pattern = {
    yyyy: '\\d{4}',
    MM: '(((0)[1-9])|((1)[0-2]))',
    dd: '([0-2][0-9]|(3)[0-1])',
    sep: '(-)'
}
let Format = {
    yyyyMMdd: '^(' + Pattern.yyyy + Pattern.sep +
        Pattern.MM + Pattern.sep + Pattern.dd + ')$',
    yyyyMM: '^(' + Pattern.yyyy + Pattern.sep + Pattern.MM + ')$',
    yyyy: '^(' + Pattern.yyyy + ')$',
}
let CustomBSDatePicker = {
    option: {
        element: undefined,
        defaultFormat: Format.yyyyMMdd + '|' + Format.yyyyMM + '|' + Format.yyyy,
        cls: 'multi_date_format'
    },
    /**
     * Clear validate status for this element.
    */
    init: function () {
        let $element = $(CustomBSDatePicker.option.element);
        let $this_parent = $element.parent().parent();
        $element.removeClass('ng-invalid ng-invalid-date ng-invalid-parse');
        $element.next().next().addClass('hide');
        $this_parent.removeClass('has-error');
    },
    /**
     * Get format from defined user on form schema.
     * If user don't defined, this pattern get default pattern.
     * Default pattern: option.defaultFormat.
     * @return {String} return pattern.
    */
    getPattern: function () {
        let def_pattern = CustomBSDatePicker.option.defaultFormat;
        let $element = $(CustomBSDatePicker.option.element);
        let pattern = $element.data('custom-format');
        return (pattern.length == 0) ? def_pattern : pattern;
    },
    /**
     * Check data input valid with defined pattern.
     * @return {Boolean} return true if value matched
    */
    isMatchRegex: function () {
        let $element = $(CustomBSDatePicker.option.element);
        let val = $element.val();
        let pattern = CustomBSDatePicker.getPattern();
        let reg = new RegExp(pattern);
        return reg.test(val);
    },
    /**
     * Check input required.
     * @return {Boolean} return true if input required
    */
    isRequired: function () {
        let $lement = $(CustomBSDatePicker.option.element);
        let $this_parent = $lement.parent().parent();
        let label = $this_parent.find('label');
        return label.hasClass('field-required');
    },
    /**
    * Get the number of days in any particular month
    * @param  {number} m The month (valid: 0-11)
    * @param  {number} y The year
    * @return {number}   The number of days in the month
    */
    daysInMonth: function (m, y) {
        switch (m) {
            case 1:
                return (y % 4 == 0 && y % 100) || y % 400 == 0 ? 29 : 28;
            case 8: case 3: case 5: case 10:
                return 30;
            default:
                return 31
        }
    },
    /**
    * Check if a date is valid
    * @param  {number}  d The day
    * @param  {number}  m The month
    * @param  {number}  y The year
    * @return {Boolean}   Returns true if valid
    */
    isValidDate: function (d, m, y) {
        let month = parseInt(m, 10) - 1;
        let checkMonth = month >= 0 && month < 12;
        let checkDay = d > 0 && d <= CustomBSDatePicker.daysInMonth(month, y);
        return checkMonth && checkDay;
    },
    /**
     * Check all validate for this.
     * All validation valid => return true.
     * @return {Boolean} Returns true if valid
    */
    isValidate: function () {
        let $element = $(CustomBSDatePicker.option.element);
        let val = $element.val();
        if (val.length == 0) {
            //Required input invalid.
            if (CustomBSDatePicker.isRequired()) return false;
        } else {
            //Data input is not match with defined pattern.
            if (!CustomBSDatePicker.isMatchRegex()) return false;
            //Check day by month and year.
            let arr = val.split('-');
            if (arr.length == 3 && !CustomBSDatePicker.isValidDate(arr[2], arr[1], arr[0])) return false;
        }
        return true;
    },
    /**
     * Check validate and apply css for this field.
    */
    validate: function () {
        let $element = $(CustomBSDatePicker.option.element);
        let $this_parent = $element.parent().parent();
        if (!CustomBSDatePicker.isValidate()) {
            $element.next().next().removeClass('hide');
            $this_parent.addClass('has-error');
        }
    },
    /**
     * This is mean function in order to validate.
     * @param {[type]} element date field
    */
    process: function (element) {
        CustomBSDatePicker.option.element = element;
        CustomBSDatePicker.init();
        CustomBSDatePicker.validate();
    },
    /**
    * Init attribute of model object if them undefine.
    * @param  {[object]}  model
    * @param  {[object]}  element is date input control.
    */
    initAttributeForModel: function (model, element) {
        if ($(element).val().length == 0) return;
        let ng_model = $(element).attr('ng-model').replace(/']/g, '');
        let arr = ng_model.split("['");
        //Init attribute of model object if them undefine.
        let str_code = '';
        $.each(arr, function (ind_01, val_02) {
            str_code += (ind_01 == 0) ? val_02 : "['" + val_02 + "']";
            let chk_str_code = '';
            if (ind_01 != arr.length - 1) {
                chk_str_code = "if(!" + str_code + ") " + str_code + "={};";
            }
            eval(chk_str_code);
        });
    },
    /**
    * Excute this function before 'Save' and 'Next' processing
    * Get data from fields in order to fill to model.
    * @param  {[object]}  model
    * @param  {[Boolean]}  reverse
    */
    setDataFromFieldToModel: function (model, reverse) {
        let cls = CustomBSDatePicker.option.cls;
        let element_arr = $('.' + cls);
        $.each(element_arr, function (ind, val) {
            CustomBSDatePicker.initAttributeForModel(model, val);
            if (reverse) {
                //Fill data from model to fields
                str_code = "$(val).val(" + $(val).attr('ng-model') + ")";
                try {
                    eval(str_code);
                } catch (e) {
                    // If the date on model is undefined, we can safetly ignore it.
                    if (!e instanceof TypeError) {
                        throw e;
                    }
                }
            } else {
                //Fill data from fields to model
                str_code = 'if ($(val).val().length != 0) {' + $(val).attr('ng-model') + '=$(val).val()}';
                eval(str_code);
            }
        });
    },
    /**
     * Get date fields name which invalid.
     * @return {array} Returns name list.
    */
    getInvalidFieldNameList: function () {
        let cls = CustomBSDatePicker.option.cls;
        let element_arr = $('.' + cls);
        let result = [];
        $.each(element_arr, function (ind, val) {
            let $element = $(val);
            let $parent = $element.parent().parent();
            if ($parent.hasClass('has-error')) {
                let name = $element.attr('name');
                let label = $("label[for=" + name + "]").text().trim();
                result.push(label);
            }
        });
        return result;
    },
    /**
     * If input empty, this attribute delete.
     * Fix bug: not enter data for date field.
    */
    removeLastAttr: function (model) {
        let cls = CustomBSDatePicker.option.cls;
        let element_arr = $('.' + cls);
        $.each(element_arr, function (ind, val) {
            if ($(val).val().length > 0) {
                CustomBSDatePicker.initAttributeForModel(model, val);
                let ng_model = $(val).attr('ng-model');
                let last_index = ng_model.lastIndexOf('[');
                let previous_attr = ng_model.substring(0, last_index);
                let str_code = "if(" + ng_model + "==''){" + previous_attr + "={}}";
                eval(str_code);
            }
        });
    }
}


const root = createRoot(document.getElementById('input_form_container'));
let forms = null;
let schema = null;

fetch('/static/json/form.json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text(); // JSONデータを取得して解析する
    })
    .then(data => {
        forms = JSON.parse(data);
        return fetch('/static/json/jsonschema.json')
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text(); // JSONデータを取得して解析する
    })
    .then(data => {
        schema = JSON.parse(data);

        root.render(<ItemRegisterPanel forms={forms} schema={schema} />);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });


