import React, { useState, useRef, createContext, useContext, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import Modal from 'react-modal';
// import { DatePicker } from 'react-datepicker';

const contentFilesContext = createContext([]);
const setContentFilesContext = createContext(null);
const thumbnailContext = createContext([]);
const setThumbnailContext = createContext(null);
const metadataContext = createContext({});
const setMetadataContext = createContext(null);
const changeMetadataContext = createContext(null);
const editMetadataContext = createContext(null);
const addFileContext = createContext(null);

const modalIsOpenContext = createContext(false);
const setModalIsOpenContext = createContext();
const modalContentContext = createContext();
const setModalContentContext = createContext();
const modalHeaderContext = createContext();
const setModalHeaderContext = createContext();

const FileProvider = ({ children }) => {
    const [contentfiles, setcontentfiles] = useState([]);
    const [thumbnail, setthumbnail] = useState([]);
    const [metadata, setmetadata] = useState({})
    const setmodalisopen = useModalIsOpenSetValue();
    const setmodalcontent = useModalContentSetValue();
    const setmodalheader = useModalHeaderSetValue();


    function changemetadata(key, value) {

        let tmpmetadata = structuredClone(metadata)
        let keylist = key.split(".")
        let meta = tmpmetadata
        for (let i = 0; i < keylist.length; i++) {
            // リスト最後の場合
            if (i === keylist.length - 1) {
                meta[keylist[i]] = value
                // それ以外
            } else {
                let tmpid = keylist[i].split("[")[0]
                let tmpid_index = keylist[i].split("[")[1].replace("]", "")
                // metadataにキーが存在しない場合
                if (!meta.hasOwnProperty(tmpid)) {
                    meta[tmpid] = []
                }
                // オブジェクトを参照
                meta = meta[tmpid]

                // tmpid_index番目の配列がないなら作る
                if (meta.length < tmpid_index - 1 || meta[tmpid_index] === undefined) {
                    meta[tmpid_index] = {}
                }
                meta = meta[tmpid_index]
            }
        }
        setmetadata(tmpmetadata)
    }

    function edit_metadata(tmpmetadata, key, value) {
        let keylist = key.split(".")
        let meta = tmpmetadata
        for (let i = 0; i < keylist.length; i++) {
            // リスト最後の場合
            if (i === keylist.length - 1) {
                meta[keylist[i]] = value
                // それ以外
            } else {
                let tmpid = keylist[i].split("[")[0]
                let tmpid_index = keylist[i].split("[")[1].replace("]", "")
                // metadataにキーが存在しない場合
                if (!meta.hasOwnProperty(tmpid)) {
                    meta[tmpid] = []
                }
                // オブジェクトを参照
                meta = meta[tmpid]

                // tmpid_index番目の配列がないなら作る
                if (meta.length < tmpid_index - 1 || meta[tmpid_index] === undefined) {
                    meta[tmpid_index] = {}
                }
                meta = meta[tmpid_index]
            }
        }
    }

    function addfiles(files, addarray) {
        const fileproperty = schema.file_info
        const contentfilenames = contentfiles.map(contentfile => contentfile.name)
        // 一時的なリストをdeepcopyで生成
        let tmpfiles = contentfiles.map(contentfile => contentfile)
        let tmpmetadata = structuredClone(metadata)
        // リストに名前が存在しないなら一時リストにプッシュ
        Array.from(files).forEach(file => {
            if (check_filesize_over_100MB(file)) {
                console.log("ファイルサイズが100MBを超えています。")
                console.log(file.name)
                setmodalisopen(true);
                setmodalheader("ファイルサイズが100MBを超えています。");
                setmodalcontent(<h4>
                    ファイル名：{file.name}
                </h4>) //現在は仮の辞書でやってる
            } else if (!(contentfilenames.includes(file.name))) {
                contentfilenames.push(file.name)
                tmpfiles.push(file)
            }
        })
        // ファイルを埋め込んだ時ファイルの名前、サイズ、mimetypeをtmpmetadataに埋め込む
        for (let i = 0; i < tmpfiles.length; i++) {
            let file = tmpfiles[i];
            edit_metadata(tmpmetadata, fileproperty.file_name.replace("[]", "[" + String(i) + "]"), file.name)
            edit_metadata(tmpmetadata, fileproperty.file_url.replace("[]", "[" + String(i) + "]"), "data/contentfiles/" + file.name)
            edit_metadata(tmpmetadata, fileproperty.file_label.replace("[]", "[" + String(i) + "]"), file.name)
            edit_metadata(tmpmetadata, fileproperty.file_format.replace("[]", "[" + String(i) + "]"), file.type)
            edit_metadata(tmpmetadata, fileproperty.file_size.replace("[]", "[" + String(i) + "]"), String(Math.round(file.size / 1024)) + " KB")
            edit_metadata(tmpmetadata, fileproperty.file_type.replace("[]", "[" + String(i) + "]"), "other")
        }
        // 一時的なリストからレンダー
        setcontentfiles(tmpfiles);
        setmetadata(tmpmetadata)
    }

    return (
        <contentFilesContext.Provider value={contentfiles}>
            <setContentFilesContext.Provider value={setcontentfiles}>
                <thumbnailContext.Provider value={thumbnail}>
                    <setThumbnailContext.Provider value={setthumbnail}>
                        <metadataContext.Provider value={metadata}>
                            <setMetadataContext.Provider value={setmetadata}>
                                <changeMetadataContext.Provider value={changemetadata}>
                                    <editMetadataContext.Provider value={edit_metadata}>
                                        <addFileContext.Provider value={addfiles}>
                                            {children}
                                        </addFileContext.Provider>
                                    </editMetadataContext.Provider>
                                </changeMetadataContext.Provider>
                            </setMetadataContext.Provider>
                        </metadataContext.Provider>
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
const useMetadataValue = () => useContext(metadataContext);
const useMetadataSetValue = () => useContext(setMetadataContext);
const useMetadataChangeValue = () => useContext(changeMetadataContext);
const useMetadataEditValue = () => useContext(editMetadataContext);
const useAddFileValue = () => useContext(addFileContext);
const ModalProvider = ({ children }) => {
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [content, setContent] = useState(""); //HTML
    const [header, setHeader] = useState(""); //文字列
    return (
        <modalIsOpenContext.Provider value={modalIsOpen}>
            <setModalIsOpenContext.Provider value={setModalIsOpen}>
                <modalHeaderContext.Provider value={content}>
                    <setModalHeaderContext.Provider value={setContent}>
                        <modalContentContext.Provider value={header}>
                            <setModalContentContext.Provider value={setHeader}>
                                {children}
                            </setModalContentContext.Provider>
                        </modalContentContext.Provider>
                    </setModalHeaderContext.Provider>
                </modalHeaderContext.Provider>
            </setModalIsOpenContext.Provider>
        </modalIsOpenContext.Provider>)
}

const useModalIsOpenValue = () => useContext(modalIsOpenContext);
const useModalIsOpenSetValue = () => useContext(setModalIsOpenContext);
const useModalHeaderValue = () => useContext(modalHeaderContext);
const useModalHeaderSetValue = () => useContext(setModalHeaderContext);
const useModalContentValue = () => useContext(modalContentContext);
const useModalContentSetValue = () => useContext(setModalContentContext);

function ItemRegisterPanel({ }) {
    let count = 0;
    const input_forms = [];
    forms.forEach(form => {
        if (!("system_prop" in schema.properties[form.key] && schema.properties[form.key].system_prop === true)) {
            input_forms.push(
                <div className="form_metadata_property" key={form.key}>
                    <Panelform form={form} />
                </div>
            )
            count++;
        }
    });
    return (
        <ModalProvider>
            <FileProvider>
                <MyModal />
                <PDFform />
                <hr />
                <div className="form">
                    {input_forms}
                </div>
                <SubmitButton />
            </FileProvider>
        </ModalProvider>
    )
}



function MyModal() {
    const modalIsOpen = useModalContentValue();
    const setModalIsOpen = useModalContentSetValue();
    const content = useModalContentValue();
    const setContent = useModalContentSetValue(); //HTML
    const header = useModalHeaderValue();
    const setHeader = useModalHeaderSetValue();

    const customStyles = {
        content: {
            top: '50%',
            left: '50%',
            right: 'auto',
            bottom: 'auto',
            width: 'auto',
            height: 'auto',
            marginRight: '-50%',
            transform: 'translate(-50%, -50%)',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            border: '0px'
        },
        overlay: {
            backgroundColor: 'rgba(0, 0, 0, 0.5)' // モーダルの背景色を半透明に設定
        }
    };

    return (
        <div>
            <Modal
                isOpen={modalIsOpen ? true : false}
                onRequestClose={() => setModalIsOpen(false)}
                style={customStyles}
                contentLabel="Example Modal">
                <div className="modal-dialog modelWidth modal-lg" role="document">
                    <div className="modal-content">
                        <div className="modal-body">
                            <div className="panel panel-default">
                                <div className="panel-heading clearfix">
                                    <h3 className="panel-title">{header}</h3>
                                </div>
                                <div className="panel-body">
                                    <div className="panel-body">
                                        <div className="row">
                                            <div className="col-sm-12 col-md-12 col-left">
                                                {content}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <br />
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-info close-button" id="btnModalClose" onClick={() => setModalIsOpen(false)}>
                                閉じる
                            </button>
                        </div>
                    </div>
                </div>
            </Modal>
        </div>
    );
}

function PDFform({ }) {
    const [pdffile, setpdffile] = useState([]);
    const addfiles = useAddFileValue();
    const contentfiles = useFilesValue();
    const setcontentfiles = useFilesSetValue();
    const thumbnail = useThumbnailValue();
    const [disabled, setdisabled] = useState(false);
    const pdfproperty = schema.pdf_info
    const metadata = useMetadataValue();
    const setmetadata = useMetadataSetValue();
    const setmodalisopen = useModalIsOpenSetValue();
    const setmodalcontent = useModalContentSetValue();
    const setmodalheader = useModalHeaderSetValue();
    const edit_metadata = useMetadataEditValue();


    function addfilesforpdf(files) {
        if (files.length > 0) {
            const firstFile = files[0];
            if (check_filesize_over_100MB(firstFile)) {
                console.log("ファイルサイズが100MBを超えています。")
                console.log(firstFile.name)
                setmodalisopen(true);
                setmodalheader("ファイルサイズが100MBを超えています。");
                setmodalcontent(<h4>
                    ファイル名：{firstFile.name}
                </h4>)
            } else if (firstFile.type === "application/pdf") {
                addfiles([firstFile])
                if (pdffile.length === 0 || pdffile[0].name !== firstFile.name) {
                    setpdffile([firstFile])
                }
            } else {
                console.log("PDFファイルではありません。")
                setmodalisopen(true);
                setmodalheader("PDFファイルではありません。");
                setmodalcontent(<h4>
                    ファイル名：{firstFile.name}
                </h4>)
            }
        } else {
            console.log("ドロップされたファイルはありません");
        }
    }

    function deletefile(filename) {
        setpdffile([]);
    }

    // ファイルをBase64にエンコードする関数
    function encodeFileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = function (event) {
                const base64Data = event.target.result.split(",")[1];
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

    function pdf_reader() {
        let files = [];
        setdisabled(true);
        encodeFilesToBase64(pdffile).then(base64files => {
            files = base64files.map(base64file => base64file)
            return request_python(files)
        }).catch(error => {
            console.error('Error encoding files:', error);
            console.log(JSON.parse(error.responseText).error)
            setmodalisopen(true);
            setmodalheader("自動入力に失敗しました。")//error.status + " " + error.statusText
            setmodalcontent(<>
            <h4>{error.status + " " + error.statusText}</h4>
            <h4>{JSON.parse(error.responseText).error}</h4>
            </>)
            setdisabled(false);
        }).finally(
        );
    }

    function request_python(files) {
        const dataforrequest = { "contentfiles": files }

        return $.ajax({
            url: "/item_register/pdf_reader",
            method: "POST",
            headers: { "Content-Type": "application/json" },
            data: JSON.stringify(dataforrequest),
            success: function (response) {
                // リクエストが成功した場合の処理
                // console.log('Success!', response);

                let tmpmetadata = structuredClone(metadata)
                let file_info = structuredClone(tmpmetadata[schema.file_info.property_name])
                let PDFresult = []
                // コンテントファイル情報以外metadataを初期化
                tmpmetadata = {}
                tmpmetadata[schema.file_info.property_name] = file_info

                // title
                if (response.title !== null && response.title !== undefined) {
                    edit_metadata(tmpmetadata, pdfproperty.title.title.replace("[]", "[0]"), response.title)
                    PDFresult.push(<h4 key={pdfproperty.properties.title}>{"・" +
                        document.getElementById(pdfproperty.properties.title).querySelector('a.panel-toggle').textContent + "：" + response.title}</h4>)
                }

                // author
                if (Array.isArray(response.author) && response.author.length !== 0) {
                    let authorList = []
                    response.author.forEach((val, index) => {
                        Object.entries(val).forEach(([k, v]) => {
                            edit_metadata(tmpmetadata, pdfproperty.author[k].replace("[]", "[" + String(index) + "]"), v)
                        })
                        authorList.push(val.creatorName)
                    })
                    PDFresult.push(<h4 key={pdfproperty.properties.author}>{"・" +
                        document.getElementById(pdfproperty.properties.author).querySelector('a.panel-toggle').textContent + "：" + authorList.join(", ")}</h4>)
                }

                // date
                if (typeof response.date === "object" && Object.keys(response.date).length !== 0 && response.date.value !== null) {
                    edit_metadata(tmpmetadata, pdfproperty.date.type.replace("[]", "[0]"), response.date.type)
                    edit_metadata(tmpmetadata, pdfproperty.date.value.replace("[]", "[0]"), response.date.value)
                    PDFresult.push(<h4 key={pdfproperty.properties.date}>{"・" +
                        document.getElementById(pdfproperty.properties.date).querySelector('a.panel-toggle').textContent + "：" + response.date.value}</h4>)
                }


                // publisher
                if (response.publisher !== null && response.publisher !== undefined) {
                    edit_metadata(tmpmetadata, pdfproperty.publisher.publisher.replace("[]", "[0]"), response.publisher)
                    PDFresult.push(<h4 key={pdfproperty.properties.publisher}>{"・" +
                        document.getElementById(pdfproperty.properties.publisher).querySelector('a.panel-toggle').textContent + "：" + response.publisher}</h4>)
                }

                // lang
                if (response.lang !== null && response.lang !== undefined) {
                    // 出力される文字コード(ISO-639-1)が違うためjpcoarのスキーマと違うためできない。ISO-639-3である必要がある。
                    // edit_metadata(tmpmetadata, pdfproperty.lang.lang.replace("[]", "[0]"), response.lang)
                    pdfproperty.lang.subproperties.forEach((k) => {
                        console.log(k)
                        if (tmpmetadata[k.split(".")[0].replace("[]", "")] !== undefined) {

                            for (let i = 0; i < tmpmetadata[k.split(".")[0].replace("[]", "")].length; i++) {
                                edit_metadata(tmpmetadata, k.replace("[]", "[" + i + "]"), response.lang)
                            }
                        }
                    })
                    PDFresult.push(<h4 key={pdfproperty.properties.lang}>{"・" +
                        document.getElementById(pdfproperty.properties.lang).querySelector('a.panel-toggle').textContent + "：" + response.lang}</h4>)
                }

                setmetadata(tmpmetadata)
                setmodalisopen(true);
                setmodalheader("自動入力完了");
                setmodalcontent(<>
                    {PDFresult}
                </>)
                setdisabled(false);
            },
            error: function (status) {
                // リクエストが失敗した場合の処理
                console.log(status)
                setdisabled(false);
            }
        })
    }

    return (
        <div className="row row-4">
            <div className="col-sm-12">
                <p className="text-center">pdf自動入力フォーム</p>
                <div className="files-upload-zone">
                    <DropFileArea addfiles={addfilesforpdf} />
                    <p className="text-center legend"><strong>— OR —</strong></p>
                    <AddFileButton addfiles={addfilesforpdf} acceptfiletype={"application/pdf"} />
                </div>
                <p className="text-center">登録可能なファイルは「pdf」のみ</p>
                <p className="text-center">
                    <button className="btn btn-success" onClick={pdf_reader} disabled={disabled}>
                        <span className="glyphicon glyphicon-plus"></span>&nbsp;
                        PDFからメタデータの自動入力
                    </button>
                </p>
                {(pdffile.length !== 0) && <Datalist contentfiles={pdffile} deletefile={deletefile} />}
            </div>
        </div>

    )
}

function SubmitButton() {
    const contentfiles = useFilesValue();
    const thumbnail = useThumbnailValue();
    const [disabled, setdisabled] = useState(false);

    const setmodalisopen = useModalIsOpenSetValue();
    const setmodalcontent = useModalContentSetValue();
    const setmodalheader = useModalHeaderSetValue();
    // ファイルをBase64にエンコードする関数
    function encodeFileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = function (event) {
                const base64Data = event.target.result.split(",")[1];
                // console.log(file.name + ":" + base64Data.length)
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
        return $.ajax({
            url: "/item_register/register",
            method: "POST",
            headers: { "Content-Type": "application/json" },
            data: JSON.stringify(dataforrequest),
            success: function (response) {
                // リクエストが成功した場合の処理
                // console.log('Success!', response);
                setmodalisopen(true);
                setmodalheader("登録成功");
                setmodalcontent(<>
                    登録先URL：<a href={response.links[0]["@id"]}>{response.links[0]["@id"]}</a>
                </>)
                setdisabled(false);
            },
            error: function (status) {
                // リクエストが失敗した場合の処理
                console.log(status)
                setdisabled(false);
            }
        })
    }

    function itemRegister() {
        const required_but_no_value = check_required(schema.required)
        if (required_but_no_value.length !== 0) {
            setmodalisopen(true)
            setmodalheader("必須項目が入力されていません。")
            setmodalcontent(<>
                {required_but_no_value.map((e) => (
                    <h4 key={e}>{"・" + document.getElementById(e).querySelector('a.panel-toggle').textContent}</h4>
                ))}</>
            )
            return 0
        }
        setdisabled(true);
        let metadata = load_metadata();
        let files = [];
        let thumb = null;
        encodeFilesToBase64(contentfiles).then(base64files => {
            files = base64files.map(base64file => base64file) // 全てのファイルのBase64データの配列が表示される
            return encodeFilesToBase64(thumbnail)
        }).then(thumbnail => {
            thumb = thumbnail.map(base64thumbnail => base64thumbnail)
            return request_python(metadata, files, thumb)
        }).catch(error => {
            console.error(error);
            setmodalisopen(true);
            setmodalheader(error.status + " " + error.statusText);
            setmodalcontent(<h4>{error.responseText}</h4>)
            setdisabled(false);
        });


    }
    return (
        <div className="row row-4">
            <div className="col-sm-12">
                <div className="col-sm-offset-3 col-sm-6">
                    <div className="list-inline text-center">

                        <button id="submit_button" className="btn btn-info next-button" disabled={disabled} onClick={itemRegister}>
                            送信
                        </button>
                    </div>
                </div>
            </div>
        </div>)
}

function FileUploadForm({ addarray, deletearray }) {
    const contentfiles = useFilesValue();
    const setcontentfiles = useFilesSetValue();
    const metadata = useMetadataValue();
    const setmetadata = useMetadataSetValue();
    const addfiles = useAddFileValue();


    function deleteFile(filename, index) {
        const fileproperty = schema.file_info
        let tmpfiles = contentfiles.map(contentfile => contentfile).filter(file => file.name !== filename)
        let tmpmetadata = structuredClone(metadata)
        tmpmetadata[fileproperty.property_name].splice(index, 1)
        deletearray()
        // 一時的なリストからレンダー
        setcontentfiles(tmpfiles);
        setmetadata(tmpmetadata)
    }

    return (
        <div className="row row-4 list-group-item">
            <div className="col-sm-12">
                <div className="files-upload-zone">
                    <DropFileArea addfiles={addfiles} />
                    <p className="text-center legend"><strong>— OR —</strong></p>
                    <AddFileButton addarray={addarray} addfiles={addfiles} />
                </div>
                {(contentfiles.length !== 0) && <Datalist contentfiles={contentfiles} deletefile={deleteFile} />}
            </div>
        </div>

    )
}

//jpcoar2.0では使わない
function ThumbnailUploadForm() {
    const thumbnail = useThumbnailValue();
    const setthumbnail = useThumbnailSetValue();
    const files = useFilesValue();
    function addfiles(files) {
        if (files.length > 0) {
            const firstFile = files[0];
            if (check_filesize_over_100MB(firstFile)) {
                console.log("ファイルサイズが100MBを超えています。")
                setmodalisopen(true);
                setmodalheader("ファイルサイズが100MBを超えています。");
                setmodalcontent(<h4>
                    ファイル名：{firstFile.name}
                </h4>)
            } else if (!(firstFile.type.startsWith('image/'))) {
                console.log("画像ファイルではありません。")
                setmodalisopen(true);
                setmodalheader("画像ファイルではありません。");
                setmodalcontent(<h4>
                    ファイル名：{firstFile.name}
                </h4>)
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


function Datalistform({ parent_id, order, value, item }) {
    return (
        <Textform value={""} order={order} item={item} parent_id={parent_id} />
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
                    {contentfiles.map((file, index) => (
                        (<tr key={file.name}>
                            <td>{file.name}</td>
                            <td>{Math.round(file.size / 1024)}KB</td>
                            <td className="text-center">
                                <a onClick={() => deletefile(file.name, index)}>
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
                    isfiles = false;
                }
            })
        } else {
            console.log("no files");
            isfiles = false;
        }
        if (isfiles === true) {
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

function AddFileButton({ addfiles, acceptfiletype, addarray }) {
    const self = useRef();
    function fileaddaction() {
        self.current.click();
    }
    return (
        <p className="text-center">
            <button className="btn btn-primary" onClick={fileaddaction} >
                Click to select
            </button>
            <input ref={self} type="file" className="hidden" multiple accept={acceptfiletype} onChange={(e) => { addfiles(e.target.files, addarray); e.target.value = ""; }} />
        </p>
    )
}

function Panelform({ parent_id, form }) {
    let form_last_key = form.key.split(".")[form.key.split(".").length - 1]
    let child_id = parent_id !== undefined ? parent_id + "." + form_last_key : form_last_key
    let isrequired = false
    // ネスト１段目のidがrequiredに含まれるならパネルを畳まない
    if (schema !== undefined && schema.required.includes(child_id)) {
        isrequired = true
    }
    const [count, setcount] = useState(1);
    const [inputlists, setInputlists] = useState([<Inputlist form={form} count={count - 1} child_id={child_id} key={form.key + "[" + String(count - 1) + "]"} />]);
    const [toggle, settoggle] = useState(isrequired ? "" : " hidden");
    const files = useFilesValue()
    const metadata = useMetadataValue();
    const setmetadata = useMetadataSetValue();
    let isArray = false;
    useEffect(() => {
        if (form.type === "contentfile") {
            let default_inputlists = []
            for (let i = 0; i < files.length; i++) {
                default_inputlists.push(<Inputlist form={form} count={i} child_id={child_id} key={form.key + "[" + String(i) + "]"} />)
            }
            setInputlists(default_inputlists)
            setcount(files.length)
        }
    }, [])
    useEffect(() => {
        let tmpmetadata = structuredClone(metadata)
        let keylist = child_id.split(".")
        let tmpmeta = tmpmetadata
        try {
            for (let i = 0; i < keylist.length; i++) {
                // リスト最後の場合
                if (i === keylist.length - 1) {
                    tmpmeta = tmpmeta[keylist[i]]
                } else {
                    let [tmp_id, tmpid_index] = keylist[i].split("[")
                    tmpid_index = tmpid_index.replace("]", "")
                    tmpmeta = tmpmeta[tmp_id][tmpid_index]
                }
            }
            if (tmpmeta.length > inputlists.length) {
                deletearray()
                let default_inputlists = []
                for (let i = 0; i < tmpmeta.length; i++) {
                    if (tmpmeta[i] !== undefined) {
                        default_inputlists.push(<Inputlist form={form} count={i} child_id={child_id} key={form.key + "[" + String(i) + "]"} />)
                    }
                }
                settoggle("")
                setInputlists(default_inputlists)
                setcount(tmpmeta.length)
            } else if (tmpmeta.length < inputlists.length) {
                let default_inputlists = []
                for (let i = 0; i < tmpmeta.length; i++) {
                    if (tmpmeta[i] !== undefined) {
                        default_inputlists.push(<Inputlist form={form} count={i} child_id={child_id} key={form.key + "[" + String(i) + "]"} />)
                    }
                }
                setInputlists(default_inputlists)
                setcount(tmpmeta.length)

            } else {
                settoggle("")
            }
        } catch (error) {
        }

    }, [metadata])

    if (form.add === "New") {
        isArray = true;
    }


    function addarray() {
        setInputlists(prevComponents => [...prevComponents,
        (<Inputlist form={form} count={count} child_id={child_id} key={form.key + "[" + String(count) + "]"} />
        )]);
        setcount(count + 1);
    }

    function reducearray(key) {
        let tmpmetadata = structuredClone(metadata)
        let keylist = child_id.split(".")
        let tmpmeta = tmpmetadata
        try {
            for (let i = 0; i < keylist.length; i++) {
                // リスト最後の場合
                if (i === keylist.length - 1) {
                    tmpmeta = tmpmeta[keylist[i]]
                } else {
                    let [tmp_id, tmpid_index] = keylist[i].split("[")
                    tmpid_index = tmpid_index.replace("]", "")
                    tmpmeta = tmpmeta[tmp_id][tmpid_index]
                }
            }
            delete tmpmeta[key.split("[")[key.split("[").length - 1].replace("]", "")]
            setmetadata(tmpmetadata)
        } catch (error) {

        } finally {
            // setTimeout(setInputlists(prevItems => prevItems.filter(inputlist => inputlist.key !== key)),0)
            setInputlists(prevItems => prevItems.filter(inputlist => inputlist.key !== key))
        }
    }

    function deletearray() {
        setcount(0)
        setInputlists([])

    }

    function togglepanel() {
        if (toggle === " hidden") {
            settoggle("")
        } else {
            settoggle(" hidden")
        }
    }

    return (
        <fieldset className="schema-form-fieldset flexbox" id={child_id} name={form.key.split(".")[form.key.split(".").length - 1]}>
            <div className="panel panel-default deposit-panel">
                <div className="panel-heading"><a className="panel-toggle" onClick={() => togglepanel()}>
                    {("title_i18n" in form) && ("ja" in form.title_i18n) ? form.title_i18n.ja : form.title}
                </a><div className="pull-right">{isrequired ? "Required" : "Optional"}</div>
                </div>
                <div className={"panel-body panel-body2 list-group" + toggle}>
                    <div className="schema-form-array">
                        <div className="col-sm-12">
                            {(form.type === "contentfile") && <FileUploadForm addarray={addarray} deletearray={deletearray} />}
                            {(form.type === "thumbnail") && <ThumbnailUploadForm addarray={addarray} deletearray={deletearray} />}
                            {inputlists.map((inputlist, index) => (
                                <li className="list-group-item ui-sortable" id={child_id + "[" + index + "]"} key={inputlist.key}>
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

function Inputlist({ form, count, child_id }) {
    // TODO　各入力formにchild_id_with_numberを引数に入れ、きれいにidが作られること
    const input_field = [];
    let child_id_with_number = child_id + "[" + count + "]"
    if (!("items" in form)) {
        input_field.push(<Datepickerform order={count} item={form} key={form.key} />);
    } else {
        form.items.forEach(item => {
            if ("type" in item) {
                if (item.type === "text") {
                    input_field.push(
                        <Textform value={""} parent_id={child_id_with_number} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "textarea") {
                    input_field.push(
                        <Textareaform parent_id={child_id_with_number} value={""} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "select") {
                    input_field.push(
                        <Selectform map={item.titleMap} parent_id={child_id_with_number} value={""} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "radios") {
                    input_field.push(
                        <Radioform map={item.titleMap} parent_id={child_id_with_number} value={""} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "fieldset") {
                    input_field.push(<Panelform form={item} parent_id={child_id_with_number} key={item.key} />);
                } else if (item.type === "contentfile" || item.type === "thumbnail") {
                    input_field.push(<Panelform form={item} parent_id={child_id_with_number} key={item.key} />);
                } else if (item.type === "template") {
                    if ("templateUrl" in item) {
                        let template = item.templateUrl.split('/').pop()
                        if (template === "datepicker.html" || template === "datepicker_multi_format.html") {
                            input_field.push(<Datepickerform order={count} parent_id={child_id_with_number} item={item} key={item.key} />);
                        } else if (template === "datalist.html") {
                            input_field.push(<Datalistform order={count} parent_id={child_id_with_number} item={item} key={item.key} />);
                        } else if (template === "checkboxes.html") {
                            input_field.push(<Checkboxesform order={count} parent_id={child_id_with_number} item={item} map={item.titleMap} key={item.key} />)
                        }
                    } else if ("template" in item) {
                        input_field.push(<div></div>);
                    }
                } else {
                    input_field.push(<div></div>);
                }

            } else {
                input_field.push(<Panelform form={item} parent_id={child_id_with_number} key={item.key} />);
            }
        })
    };
    return (
        <div className="list-group">
            {input_field}
        </div>
    );
}

function Metadatatitle({ item }) {
    let required = false;
    let title = ("title_i18n" in item) && ("ja" in item.title_i18n) ? item.title_i18n.ja : item.title
    let classvalue;
    if (schema.required.includes(item.key.split(".")[0].replace("[]", ""))) {
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

function Textform({ item, parent_id }) {
    const metadata = useMetadataValue();
    const changemetadata = useMetadataChangeValue();
    const form_id = parent_id + "." + item.key.split(".")[item.key.split(".").length - 1]
    let readonly = false;

    // とりあえず今はコメントアウト
    if ("readonly" in item && item.readonly === true) {
        readonly = true;
    }
    return (
        <div className="form-group schema-form-text">
            <Metadatatitle item={item} />
            <div className="col-sm-9">
                <input type="text"
                    className="form-control input-form"
                    id={form_id}
                    name={item.key.split(".")[item.key.split(".").length - 1]}
                    schema-validate="form"
                    disabled={readonly}
                    defaultValue={getmetadata(form_id, metadata)}
                    onBlur={(e) => changemetadata(form_id, e.target.value)}
                ></input>
            </div>
        </div>
    );
}


function Selectform({ parent_id, map, item }) {
    const metadata = useMetadataValue();
    const edit_metadata = useMetadataEditValue();
    const setmetadata = useMetadataSetValue();
    const titlemap = [];
    const form_id = parent_id + "." + item.key.split(".")[item.key.split(".").length - 1]
    function selectonchange(form_id, value) {
        // change select value
        let tmpmetadata = structuredClone(metadata)
        edit_metadata(tmpmetadata, form_id, value)
        // use onchange
        if (item.hasOwnProperty("onChange")) {
            const onchange = item.onChange
            edit_metadata(tmpmetadata, parent_id + "." + onchange.changekey, onchange.keyvalue[value])
        }
        setmetadata(tmpmetadata)
    }
    map.forEach(element => {
        titlemap.push(
            <option label={element.name} value={element.value} key={form_id + element.value}></option>
        );
    })
    return (
        <div className="form-group schema-form-select">
            <Metadatatitle item={item} />
            <div className="col-sm-9">
                <select className="form-control input-form"
                    schema-validate="form"
                    id={form_id}
                    name={item.key.split(".")[item.key.split(".").length - 1]}
                    value={getmetadata(form_id, metadata) || ""}
                    onChange={(e) => selectonchange(form_id, e.target.value)}>
                    <option value=""></option>
                    {titlemap}
                </select>
            </div>
        </div>

    )
}

// いまはとりあえず　input date型である。
function Datepickerform({ parent_id, item }) {
    const changemetadata = useMetadataChangeValue();
    const metadata = useMetadataValue();
    const form_id = parent_id + "." + item.key.split(".")[item.key.split(".").length - 1]
    return (
        <div className="form-group schema-form-datepicker">
            <Metadatatitle item={item} />

            <div className="col-sm-9">
                <input type="date"
                    className="form-control input-form"
                    id={form_id}
                    name={item.key.split(".")[item.key.split(".").length - 1]}
                    schema-validate="form"
                    defaultValue={getmetadata(form_id, metadata)}
                    onBlur={(e) => changemetadata(form_id, e.target.value)}
                ></input>
            </div>
        </div>
    )
}

function Textareaform({ parent_id, item }) {
    const changemetadata = useMetadataChangeValue();
    const metadata = useMetadataValue();
    const form_id = parent_id + "." + item.key.split(".")[item.key.split(".").length - 1]
    return (
        <div className="form-group schema-form-textarea">
            <Metadatatitle item={item} />
            <div className="col-sm-9">
                <textarea className="form-control input-form"
                    id={form_id}
                    name={item.key.split(".")[item.key.split(".").length - 1]}
                    schema-validate="form"
                    defaultValue={getmetadata(form_id, metadata)}
                    onBlur={(e) => changemetadata(form_id, e.target.value)}
                ></textarea>
            </div>
        </div>
    );
}



// 未完成jpcoar2.0では使わない
function Radioform({ parent_id, map, order, value, item }) {
    const titlemap = [];
    map.forEach(element => {
        titlemap.push(
            <div className="radio">
                <label>
                    <input type="radio"
                        id={parent_id + "." + item.key.split(".")[item.key.split(".").length - 1]}
                        name={item.key.replaceAll("[]", "[" + String(order) + "]")}
                        value={element.value} />
                    <span ng-bind-html="item.name">{element.name_i18n.ja}</span>
                </label>
            </div >
        );
    })

    return (
        <div className="form-group schema-form-radios">
            <Metadatatitle item={item} />
            <div className="col-sm-9">
                {titlemap}
            </div>
        </div>
    )
}




// 未完成jpcoar2.0では使わない
function Checkboxesform({ parent_id, order, value, item }) {
    const titlemap = [];
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
            <Metadatatitle item={item} />
            <div className="col-sm-9">
                <div className="checkbox">
                    <select sf-changed="form" className="form-control" schema-validate="form" id={parent_id + "." + item.key.split(".")[item.key.split(".").length - 1]} defaultValue={value}>
                        <option className value=""></option>
                        {titlemap}
                    </select>
                </div>
            </div>
        </div>
    )
}

function getmetadata(key, metadata) {
    let keylist = key.split(".")
    let tmpmeta = metadata
    try {
        for (let i = 0; i < keylist.length; i++) {
            // リスト最後の場合
            if (i === keylist.length - 1) {
                return tmpmeta[keylist[i]]
            } else {
                let [tmp_id, tmpid_index] = keylist[i].split("[")
                tmpid_index = tmpid_index.replace("]", "")
                tmpmeta = tmpmeta[tmp_id][tmpid_index]
            }
        }
    } catch (error) {
        return undefined
    }
    return tmpmeta
}

function load_panel(panel, property, nest) {
    panel.querySelectorAll('.schema-form-fieldset').forEach(function (element) {
        if (element.id.split(".").length === nest) {
            property[element.name] = []
            let propers = property[element.name]
            element.querySelectorAll('li.list-group-item.ui-sortable').forEach(function (elem) {
                if (elem.id.split(".").length === nest) {
                    let proper = {}
                    elem.querySelectorAll('.input-form.form-control').forEach(function (e) {
                        if (e.id.split('.').length <= nest + 1) {
                            if (e.value !== "")
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
            if (elemen.id.split(".").length === 1) {
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

function check_required(required_list) {
    let required_but_no_value_list = new Set();
    required_list.forEach(function (element) {
        const required_panel = document.getElementById(element);
        required_panel.querySelectorAll('.input-form.form-control').forEach(function (ele) {
            if (ele.value === undefined || ele.value === "") {
                ele.style.border = '1px solid red';
                required_but_no_value_list.add(element);
            } else {
                ele.style.border = '';
            }
        })
    })
    return Array.from(required_but_no_value_list);
}

function check_filesize_over_100MB(file) {
    /// ファイルサイズ取得
    const fileSize = file.size;
    /// MB単位のファイルサイズ計算
    const fileMib = fileSize / 1024 ** 2;
    if (fileMib < 100) {
        return false
    } else {
        return true
    }
}

const root = createRoot(document.getElementById('input_form_container'));
Modal.setAppElement(document.getElementById('input_form_container'));
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
        root.render(<ItemRegisterPanel />);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });


