import React, { useState, useRef, createContext, useContext, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import Modal from 'react-modal';
// import { DatePicker } from 'react-datepicker';
const OVER_100MB_MESSAGE = "ファイルサイズが100MBを超えています。";
const FETCH_ERROR_MESSAGE = "There was a problem with the fetch operation";
const NETWORK_ERROR_MESSAGE = "'Network response was not ok'";

const contentFilesContext = createContext([]);
const setContentFilesContext = createContext(null);
const thumbnailContext = createContext([]);
const setThumbnailContext = createContext(null);
const metadataContext = createContext({});
const setMetadataContext = createContext(null);
const changeMetadataContext = createContext(null);
const editMetadataContext = createContext(null);
const addFileContext = createContext(null);
const autoInfoEntryContext = createContext(null);
const autoInfoEntrySetContext = createContext(null);

const modalIsOpenContext = createContext(false);
const setModalIsOpenContext = createContext();
const modalContentContext = createContext();
const setModalContentContext = createContext();
const modalHeaderContext = createContext();
const setModalHeaderContext = createContext();

const FileProvider = ({ children }) => {
    const [contentFiles, setContentFiles] = useState([]);
    const [thumbnail, setThumbnail] = useState([]);
    const [metadata, setMetadata] = useState({})
    const [isAutoInput, setIsAutoInput] = useState(false)
    const setModalIsOpen = useModalIsOpenSetValue();
    const setModalContent = useModalContentSetValue();
    const setModalHeader = useModalHeaderSetValue();

    /**
    この関数はkeyが表す位置の辞書metadataの値を変更します。
    また、keyが表す位置の辞書のキーがない場合、キーを作成します。
    その後、再レンダリングをおこないます。
    @param {string} key 追加するkeyです。 例："dc:title[0].dc:title"
    @param {string} value keyに対応するvalueです。　例 "タイトル"
    @return なし
    */
    function changeMetadata(key, value) {
        /*
        */

        let tmpMetadata = structuredClone(metadata)
        let keyList = key.split(".")
        let meta = tmpMetadata
        for (let i = 0; i < keyList.length; i++) {
            // リスト最後の場合
            if (i === keyList.length - 1) {
                meta[keyList[i]] = value
                // それ以外
            } else {
                let tmpId = keyList[i].split("[")[0]
                let tmpIdIndex = keyList[i].split("[")[1].replace("]", "")
                // metadataにキーが存在しない場合
                if (!meta.hasOwnProperty(tmpId)) {
                    meta[tmpId] = []
                }
                // オブジェクトを参照
                meta = meta[tmpId]

                // tmpIdIndex番目の配列がないなら作る
                if (meta.length < tmpIdIndex - 1 || meta[tmpIdIndex] === undefined) {
                    meta[tmpIdIndex] = {}
                }
                meta = meta[tmpIdIndex]
            }
        }
        setMetadata(tmpMetadata)
    }

    /**
    * このメソッドは渡された辞書tmpMetadataにkey,valueを追加、または上書きします。
    * 参照渡しされた辞書を編集するので返り値はありません。
    * このメソッドでは再レンダリングを行いません。
    * メソッド後のtmpMetadata：tmpMetadata = {"dc:title":[{"dc:title":"タイトル"},null,{}]}
    * @param {dict} tmpMetadata 編集する辞書を想定しています。
    * @param {string} key 追加するkeyです。 例："dc:title[0].dc:title"
    * @param {string} value keyに対応するvalueです。　例 "タイトル"
    * @return なし
    */
    function editMetadata(tmpMetadata, key, value) {
        let keyList = key.split(".")
        let meta = tmpMetadata
        for (let i = 0; i < keyList.length; i++) {
            // リスト最後の場合
            if (i === keyList.length - 1) {
                meta[keyList[i]] = value
                // それ以外
            } else {
                let tmpId = keyList[i].split("[")[0]
                let tmpIdIndex = keyList[i].split("[")[1].replace("]", "")
                // metadataにキーが存在しない場合
                if (!meta.hasOwnProperty(tmpId)) {
                    meta[tmpId] = []
                }
                // オブジェクトを参照
                meta = meta[tmpId]

                // tmpIdIndex番目の配列がないなら作る
                if (meta.length < tmpIdIndex - 1 || !meta[tmpIdIndex]) {
                    meta[tmpIdIndex] = {}
                }
                meta = meta[tmpIdIndex]
            }
        }
    }

    /**
     * このメソッドは受け取ったFileListオブジェクトをFileオブジェクトに分割し、
     * contentFilesに入れることを目的にしています。
     * また、contentFilesに入ったFileオブジェクトから各情報を取り出し、ファイル情報に自動入力します。
     * @param {FileList} files 
     * @return なし
     */
    function addFiles(files) {
        const fileProperty = schema.file_info
        const contentFileNames = contentFiles.map(contentfile => contentfile.name)
        // 一時的なリストをdeepcopyで生成
        let tmpFiles = contentFiles.map(contentfile => contentfile)
        let tmpMetadata = structuredClone(metadata)
        // リストに名前が存在しないなら一時リストにプッシュ
        Array.from(files).forEach(file => {
            if (checkFilesizeOver100MB(file)) {
                setModalIsOpen(true);
                setModalHeader(OVER_100MB_MESSAGE);
                setModalContent(<h4>
                    ファイル名：{file.name}
                </h4>)
            } else if (!(contentFileNames.includes(file.name))) {
                contentFileNames.push(file.name)
                tmpFiles.push(file)
            }
        })
        // ファイルを埋め込んだ時ファイルの名前、サイズ、mimetypeをtmpMetadataに埋め込む
        for (let i = 0; i < tmpFiles.length; i++) {
            let file = tmpFiles[i];
            const idx = "[" + String(i) + "]"
            editMetadata(tmpMetadata, fileProperty.file_name.replace("[]", idx), file.name)
            editMetadata(tmpMetadata, fileProperty.file_url.replace("[]", idx), "data/contentfiles/" + file.name)
            editMetadata(tmpMetadata, fileProperty.file_label.replace("[]", idx), file.name)
            editMetadata(tmpMetadata, fileProperty.file_format.replace("[]", idx), file.type)
            editMetadata(tmpMetadata, fileProperty.file_size.replace("[]", idx), String(Math.round(file.size / 1024)) + " KB")
            editMetadata(tmpMetadata, fileProperty.file_type.replace("[]", idx), "other")
        }
        // 一時的なリストからレンダー
        setContentFiles(tmpFiles);
        setMetadata(tmpMetadata);
        setIsAutoInput(true);
    }

    return (
        <contentFilesContext.Provider value={contentFiles}>
            <setContentFilesContext.Provider value={setContentFiles}>
                <thumbnailContext.Provider value={thumbnail}>
                    <setThumbnailContext.Provider value={setThumbnail}>
                        <metadataContext.Provider value={metadata}>
                            <setMetadataContext.Provider value={setMetadata}>
                                <changeMetadataContext.Provider value={changeMetadata}>
                                    <editMetadataContext.Provider value={editMetadata}>
                                        <addFileContext.Provider value={addFiles}>
                                            <autoInfoEntryContext.Provider value={isAutoInput}>
                                                <autoInfoEntrySetContext.Provider value={setIsAutoInput}>
                                                    {children}
                                                </autoInfoEntrySetContext.Provider>
                                            </autoInfoEntryContext.Provider>
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
const useAutoInfoEntryValue = () => useContext(autoInfoEntryContext);
const useAutoInfoEntrySetValue = () => useContext(autoInfoEntrySetContext);

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

function ItemRegisterTabPage({ }) {
    let count = 0;
    const inputForms = [];
    const SYSTEM_PROP = "system_prop"
    forms.filter((form) => !(SYSTEM_PROP in schema.properties[form.key] && schema.properties[form.key][SYSTEM_PROP] === true))
        .forEach(form => {
            inputForms.push(
                <div className="form_metadata_property" key={form.key}>
                    <Panelform form={form} />
                </div>
            )
            count++;
        });
    return (
        <ModalProvider>
            <FileProvider>
                <WrappedModal />
                <PDFform />
                <hr />
                <div className="form">
                    {inputForms}
                </div>
                <SubmitButton />
            </FileProvider>
        </ModalProvider>
    )
}



function WrappedModal() {
    const modalIsOpen = useModalIsOpenValue();
    const setModalIsOpen = useModalIsOpenSetValue();
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
    const [pdfFile, setPdfFile] = useState([]);
    const addFiles = useAddFileValue();
    const [disabled, setDisabled] = useState(false);
    const pdfProperty = schema.pdf_info
    const metadata = useMetadataValue();
    const setIsAutoInput = useAutoInfoEntrySetValue();
    const setMetadata = useMetadataSetValue();
    const setModalIsOpen = useModalIsOpenSetValue();
    const setModalContent = useModalContentSetValue();
    const setModalHeader = useModalHeaderSetValue();
    const editMetadata = useMetadataEditValue();

    /**
     * このメソッドは引数filesから一番目のPDFファイルをFileオブジェクトとして取り出すことを目的にしています。
     * 取り出されたFileオブジェクトはpdfFile、contentFilesに追加、上書きされます。
     * @param {FileList} files 
     */
    function addFilesForPdf(files) {
        if (files.length > 0) {
            const firstFile = files[0];
            if (checkFilesizeOver100MB(firstFile)) {
                setModalIsOpen(true);
                setModalHeader(OVER_100MB_MESSAGE);
                setModalContent(<h4>
                    ファイル名：{firstFile.name}
                </h4>)
            } else if (firstFile.type === "application/pdf") {
                addFiles([firstFile])
                if (pdfFile.length === 0 || pdfFile[0].name !== firstFile.name) {
                    setPdfFile([firstFile])
                }
            } else {
                setModalIsOpen(true);
                setModalHeader("PDFファイルではありません。");
                setModalContent(<h4>
                    ファイル名：{firstFile.name}
                </h4>)
            }
        } else {
            console.log("ドロップされたファイルはありません");
        }
    }
    /**
     * このメソッドはpdfFileのFileオブジェクトを削除することを目的にしています。
     */
    function deleteFile() {
        setPdfFile([]);
    }

    /**
     * このメソッドはFileオブジェクトをBase64にエンコードすることを目的にしています。
     * ただ、返り値はPromiseです。
     * @param {File} file 
     * @returns {Promise}
     */
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

    /**
     * このメソッドはFileオブジェクトのリストをまとめてBase64にエンコードすることを目的にしています。
     * encodeFileToBase64は返り値がPromiseなのでPromise.allをして返り値を返しています。
     * @param {Array} files 
     * @returns {result}
     */
    function encodeFilesToBase64(files) {
        const promises = files.map(file => {
            return encodeFileToBase64(file)
        });
        return Promise.all(promises);
    }

    /**
     * このメソッドはpdfFileにあるPDFをエンコードし、pythonに送ることを目的にしています。
     * @return 
     */
    function readPdf() {
        let files = [];
        setDisabled(true);
        encodeFilesToBase64(pdfFile).then(base64files => {
            files = base64files.map(base64file => base64file)
            return requestPython(files)
        }).catch(error => {
            setModalIsOpen(true);
            setModalHeader("自動入力に失敗しました。")
            setModalContent(<>
                <h4>{error.status + " " + error.statusText}</h4>
                <h4>{JSON.parse(error.responseText).error}</h4>
            </>)
            setDisabled(false);
        }).finally(
        );
    }

    /**
     * このメソッドはbase64エンコードされたPDFファイルから抽出した情報を自動入力することを目的にしています。
     * POSTrequest送信後responseとしてはPDFファイルから抽出した情報が返ってきます。
     * {"title":"タイトル", "author":[], "date":{"object":"", "value":""}}などが考えられます。
     * @param {Array} files 
     * @returns 
     */
    function requestPython(files) {
        const dataForRequest = { "contentfiles": files }

        return $.ajax({
            url: "/item_register/pdf_reader",
            method: "POST",
            headers: { "Content-Type": "application/json" },
            data: JSON.stringify(dataForRequest),
            success: function (response) {

                let tmpMetadata = structuredClone(metadata)
                let fileInfo = structuredClone(tmpMetadata[schema.file_info.property_name])
                let PDFresult = []

                // pdf自動入力される可能性があるmetadataを初期化
                Object.keys(pdfProperty.properties).forEach((key) => {
                    delete tmpMetadata[pdfProperty.properties[key]]
                })
                tmpMetadata[schema.file_info.property_name] = fileInfo

                // title
                if (response.title !== null && response.title !== undefined) {
                    editMetadata(tmpMetadata, pdfProperty.title.title.replace("[]", "[0]"), response.title)
                    PDFresult.push(<h4 key={pdfProperty.properties.title}>{"・" +
                        document.getElementById(pdfProperty.properties.title).querySelector('a.panel-toggle').textContent + "：" + response.title}</h4>)
                }

                // author
                if (Array.isArray(response.author) && response.author.length !== 0) {
                    let authorList = []
                    response.author.forEach((val, index) => {
                        Object.entries(val).forEach(([k, v]) => {
                            editMetadata(tmpMetadata, pdfProperty.author[k].replace("[]", "[" + String(index) + "]"), v)
                        })
                        authorList.push(val.creatorName)
                    })
                    PDFresult.push(<h4 key={pdfProperty.properties.author}>{"・" +
                        document.getElementById(pdfProperty.properties.author).querySelector('a.panel-toggle').textContent + "：" + authorList.join(", ")}</h4>)
                }

                // date
                if (typeof response.date === "object" && Object.keys(response.date).length !== 0 && response.date.value !== null) {
                    editMetadata(tmpMetadata, pdfProperty.date.type.replace("[]", "[0]"), response.date.type)
                    editMetadata(tmpMetadata, pdfProperty.date.value.replace("[]", "[0]"), response.date.value)
                    PDFresult.push(<h4 key={pdfProperty.properties.date}>{"・" +
                        document.getElementById(pdfProperty.properties.date).querySelector('a.panel-toggle').textContent + "：" + response.date.value}</h4>)
                }


                // publisher
                if (response.publisher !== null && response.publisher !== undefined) {
                    editMetadata(tmpMetadata, pdfProperty.publisher.publisher.replace("[]", "[0]"), response.publisher)
                    PDFresult.push(<h4 key={pdfProperty.properties.publisher}>{"・" +
                        document.getElementById(pdfProperty.properties.publisher).querySelector('a.panel-toggle').textContent + "：" + response.publisher}</h4>)
                }

                // lang
                if (response.lang !== null && response.lang !== undefined) {
                    // 出力される文字コード(ISO-639-1)が違うためjpcoarのスキーマと違うためできない。ISO-639-3である必要がある。
                    // editMetadata(tmpMetadata, pdfProperty.lang.lang.replace("[]", "[0]"), response.lang)
                    pdfProperty.lang.subproperties.forEach((k) => {
                        if (tmpMetadata[k.split(".")[0].replace("[]", "")] !== undefined) {

                            for (let i = 0; i < tmpMetadata[k.split(".")[0].replace("[]", "")].length; i++) {
                                editMetadata(tmpMetadata, k.replace("[]", "[" + i + "]"), response.lang)
                            }
                        }
                    })
                    PDFresult.push(<h4 key={pdfProperty.properties.lang}>{"・" +
                        document.getElementById(pdfProperty.properties.lang).querySelector('a.panel-toggle').textContent + "：" + response.lang}</h4>)
                }

                setMetadata(tmpMetadata)
                setIsAutoInput(true)
                setModalIsOpen(true);
                setModalHeader("自動入力完了");
                setModalContent(<>
                    {PDFresult}
                </>)
                setDisabled(false);
            },
            error: function (status) {
                setDisabled(false);
            }
        })
    }

    return (
        <div className="row row-4">
            <div className="col-sm-12">
                <p className="text-center">pdf自動入力フォーム</p>
                <div className="files-upload-zone">
                    <DropFileArea addFiles={addFilesForPdf} />
                    <p className="text-center legend"><strong>— OR —</strong></p>
                    <AddFileButton addFiles={addFilesForPdf} acceptFileType={"application/pdf"} />
                </div>
                <p className="text-center">登録可能なファイルは「pdf」のみ</p>
                <p className="text-center">
                    <button className="btn btn-success" onClick={readPdf} disabled={disabled}>
                        <span className="glyphicon glyphicon-plus"></span>&nbsp;
                        PDFからメタデータの自動入力
                    </button>
                </p>
                {(pdfFile.length !== 0) && <Datalist contentFiles={pdfFile} deleteFile={deleteFile} />}
            </div>
        </div>

    )
}

function SubmitButton() {
    const contentFiles = useFilesValue();
    const thumbnail = useThumbnailValue();
    const [disabled, setDisabled] = useState(false);

    const setModalIsOpen = useModalIsOpenSetValue();
    const setModalContent = useModalContentSetValue();
    const setModalHeader = useModalHeaderSetValue();

    /**
     * このメソッドはFileオブジェクトをBase64にエンコードすることを目的にしています。
     * ただ、返り値はPromiseです。
     * @param {File} file 
     * @returns {Promise}
     */
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

    /**
     * このメソッドはFileオブジェクトのリストをまとめてBase64にエンコードすることを目的にしています。
     * encodeFileToBase64は返り値がPromiseなのでPromise.allをして返り値を返しています。
     * @param {Array} files 
     * @returns {result}
     */
    function encodeFilesToBase64(files) {
        const promises = files.map(file => {
            return encodeFileToBase64(file)
        });
        return Promise.all(promises);
    }

    /**
     * 入力されたmetadata、files、thumbをpythonに送ることを目的にしています。
     * POSTrequest送信後ステータスコード200の場合responseとしては登録したリポジトリのURLが返ってきます。
     * @param {dict} metadata 画面に入力された情報を辞書型で成形したものです。
     * @param {Array} files contentFilesに入っていたFileオブジェクトをlistにいれたものです。
     * @param {Array} thumb thumbnailに入っていたFileオブジェクトをlistにいれたものです。
     * @returns 
     */
    function requestPython(metadata, files, thumb) {
        const dataForRequest = { "item_metadata": metadata, "contentfiles": files, "thumbnail": thumb }
        return $.ajax({
            url: "/item_register/register",
            method: "POST",
            headers: { "Content-Type": "application/json" },
            data: JSON.stringify(dataForRequest),
            success: function (response) {
                setModalIsOpen(true);
                setModalHeader("登録成功");
                setModalContent(<>
                    登録先URL：<a href={response.links[0]["@id"]}>{response.links[0]["@id"]}</a>
                </>)
                setDisabled(false);
            },
            error: function (status) {
                console.log(status)
                setDisabled(false);
            }
        })
    }

    /**
     * このメソッドは入力された情報をreadMetadataメソッドであつめ、pythonに送ることを目的にしています。
     * なお、必須事項のチェックがcheckRequiredで入ります。
     * @returns 
     */
    function itemRegister() {
        const requiredButNoValue = checkRequired(schema.required)
        if (requiredButNoValue.length !== 0) {
            setModalIsOpen(true)
            setModalHeader("必須項目が入力されていません。")
            setModalContent(<>
                {requiredButNoValue.map((e) => (
                    <h4 key={e}>{"・" + document.getElementById(e).querySelector('a.panel-toggle').textContent}</h4>
                ))}</>
            )
            return 0
        }
        setDisabled(true);
        let metadata = readMetadata();
        let files = [];
        let thumb = null;
        encodeFilesToBase64(contentFiles).then(base64files => {
            files = base64files.map(base64file => base64file) // 全てのファイルのBase64データの配列が表示される
            return encodeFilesToBase64(thumbnail)
        }).then(thumbnail => {
            thumb = thumbnail.map(base64thumbnail => base64thumbnail)
            return requestPython(metadata, files, thumb)
        }).catch(error => {
            console.error(error);
            setModalIsOpen(true);
            setModalHeader(error.status + " " + error.statusText);
            setModalContent(<h4>{error.responseText}</h4>)
            setDisabled(false);
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

function FileUploadForm({ addArray, deleteArray }) {
    const contentFiles = useFilesValue();
    const setContentFiles = useFilesSetValue();
    const metadata = useMetadataValue();
    const setMetadata = useMetadataSetValue();
    const addFiles = useAddFileValue();
    const setIsAutoInput = useAutoInfoEntrySetValue();


    function deleteFile(filename, index) {
        const fileProperty = schema.file_info
        let tmpFiles = contentFiles.map(contentfile => contentfile).filter(file => file.name !== filename)
        let tmpMetadata = structuredClone(metadata)
        tmpMetadata[fileProperty.property_name].splice(index, 1)
        deleteArray()
        // 一時的なリストからレンダー
        setIsAutoInput(true)
        setContentFiles(tmpFiles);
        setMetadata(tmpMetadata)
    }

    return (
        <div className="row row-4 list-group-item">
            <div className="col-sm-12">
                <div className="files-upload-zone">
                    <DropFileArea addFiles={addFiles} />
                    <p className="text-center legend"><strong>— OR —</strong></p>
                    <AddFileButton addArray={addArray} addFiles={addFiles} />
                </div>
                {(contentFiles.length !== 0) && <Datalist contentFiles={contentFiles} deleteFile={deleteFile} />}
            </div>
        </div>

    )
}

//jpcoar2.0では使わない
/*
function ThumbnailUploadForm() {
    const thumbnail = useThumbnailValue();
    const setThumbnail = useThumbnailSetValue();
    const files = useFilesValue();
    function addFiles(files) {
        if (files.length > 0) {
            const firstFile = files[0];
            if (checkFilesizeOver100MB(firstFile)) {
                console.log(OVER_100MB_MESSAGE)
                setModalIsOpen(true);
                setModalHeader(OVER_100MB_MESSAGE);
                setModalContent(<h4>
                    ファイル名：{firstFile.name}
                </h4>)
            } else if (!(firstFile.type.startsWith('image/'))) {
                console.log("画像ファイルではありません。")
                setModalIsOpen(true);
                setModalHeader("画像ファイルではありません。");
                setModalContent(<h4>
                    ファイル名：{firstFile.name}
                </h4>)
            } else {
                setThumbnail([firstFile]);
            }
        } else {
            console.log("ドロップされたファイルはありません");
        }
    }
    function deleteFile(filename) {
        setThumbnail([]);
    }

    return (
        <div className="row row-4 list-group-item">
            <div className="col-sm-12">
                <div className="files-upload-zone">
                    <DropFileArea addFiles={addFiles} />
                    <p className="text-center legend"><strong>— OR —</strong></p>
                    <AddFileButton addFiles={addFiles} acceptFileType={"image/*"} />
                </div>
                <p className="text-center">登録可能なファイルは「gif, jpg, jpe, jpeg, png, bmp」</p>
                {(thumbnail.length !== 0) && <Datalist contentFiles={thumbnail} deleteFile={deleteFile} />}
            </div>
        </div>

    )
}
*/

function FileNameform({ parentId, order, value, item }) {
    return (
        <Textform value={""} order={order} item={item} parentId={parentId} />
    )
}

function Datalist({ contentFiles, deleteFile }) {
    return (
        <div className="panel panel-default">
            <div className="panel-heading">
                <div className="row">
                    <div className="col-sm-6">
                    </div>
                </div>
            </div>
            <table className="table">
                <tbody>
                    <tr>
                        <th>Filename</th>
                        <th>Size</th>
                        <th className="text-center">Actions</th>
                    </tr>
                    {contentFiles.map((file, index) => (
                        (<tr key={file.name}>
                            <td>{file.name}</td>
                            <td>{Math.round(file.size / 1024)}KB</td>
                            <td className="text-center">
                                <a onClick={() => deleteFile(file.name, index)}>
                                    削除
                                </a>
                            </td>
                        </tr>)
                    ))}
                </tbody>
            </table>
            <div className="panel-footer"></div>
        </div>
    )
}

function DropFileArea({ addFiles }) {

    function dragOverHandler(event) {
        event.preventDefault()
    }

    function dropFile(event) {
        event.preventDefault();
        let isFiles = true;
        if (event.dataTransfer.files) {
            [...event.dataTransfer.items].forEach((item) => {
                // ドロップしたものがファイルでない場合は拒否する
                if (item.kind !== "file") {
                    isFiles = false;
                }
            })
        } else {
            console.log("no files");
            isFiles = false;
        }
        if (isFiles === true) {
            addFiles(event.dataTransfer.files)
        }
    }

    return (
        <div className="well" onDragOver={(e) => { dragOverHandler(e) }} onDrop={(e) => { dropFile(e) }}>
            <center>
                Drop files or folders here
            </center>
        </div>)
}

function AddFileButton({ addFiles, acceptFileType, addArray }) {
    const self = useRef();
    function fileAddAction() {
        self.current.click();
    }
    return (
        <p className="text-center">
            <button className="btn btn-primary" onClick={fileAddAction} >
                Click to select
            </button>
            <input ref={self} type="file" className="hidden" multiple accept={acceptFileType} onChange={(e) => { addFiles(e.target.files, addArray); e.target.value = ""; }} />
        </p>
    )
}

function Panelform({ parentId, form }) {
    let formLastKey = form.key.split(".")[form.key.split(".").length - 1]
    let childId = parentId !== undefined ? parentId + "." + formLastKey : formLastKey
    let isRequired = false
    // ネスト１段目のidがrequiredに含まれるならパネルを畳まない
    if (schema !== undefined && schema.required.includes(childId)) {
        isRequired = true
    }
    const [count, setCount] = useState(1);
    const [inputlists, setInputlists] = useState([<Inputlist form={form} count={count - 1} childId={childId} key={form.key + "[" + String(count - 1) + "]"} />]);
    const [toggle, setToggle] = useState(isRequired ? "" : " hidden");
    const files = useFilesValue()
    const metadata = useMetadataValue();
    const setMetadata = useMetadataSetValue();
    const isAutoInput = useAutoInfoEntryValue();
    const setIsAutoInput = useAutoInfoEntrySetValue();
    let isArray = false;
    useEffect(() => {
        if (form.type === "contentfile") {
            let defaultInputlists = []
            for (let i = 0; i < files.length; i++) {
                defaultInputlists.push(<Inputlist form={form} count={i} childId={childId} key={form.key + "[" + String(i) + "]"} />)
            }
            setInputlists(defaultInputlists)
            setCount(files.length)
        }
    }, [])
    useEffect(() => {
        if (isAutoInput === true) {
            deleteArray()
            setIsAutoInput(false)
        } else {
            let tmpMetadata = structuredClone(metadata)
            let keyList = childId.split(".")
            let tmpMeta = tmpMetadata
            try {
                for (let i = 0; i < keyList.length; i++) {
                    // リスト最後の場合
                    if (i === keyList.length - 1) {
                        tmpMeta = tmpMeta[keyList[i]]
                    } else {
                        let [tmpId, tmpIdIndex] = keyList[i].split("[")
                        tmpIdIndex = tmpIdIndex.replace("]", "")
                        tmpMeta = tmpMeta[tmpId][tmpIdIndex]
                    }
                }

                let defaultInputlists = []
                for (let i = 0; i < tmpMeta.length; i++) {
                    if (tmpMeta[i] !== undefined) {
                        defaultInputlists.push(<Inputlist form={form} count={i} childId={childId} key={form.key + "[" + String(i) + "]"} />)
                    }
                }
                setToggle("")
                setInputlists(defaultInputlists)
                setCount(tmpMeta.length)


            } catch (error) {
                setCount(1)
                setInputlists([<Inputlist form={form} count={0} childId={childId} key={form.key + "[" + String(0) + "]"} />])
            } finally {
            }
        }

    }, [isAutoInput])

    if (form.add === "New") {
        isArray = true;
    }


    function addArray() {
        setInputlists(prevComponents => [...prevComponents,
        (<Inputlist form={form} count={count} childId={childId} key={form.key + "[" + String(count) + "]"} />
        )]);
        setCount(count + 1);
    }

    function reducearray(key) {
        let tmpMetadata = structuredClone(metadata)
        let keyList = childId.split(".")
        let tmpMeta = tmpMetadata
        try {
            for (let i = 0; i < keyList.length; i++) {
                // リスト最後の場合
                if (i === keyList.length - 1) {
                    tmpMeta = tmpMeta[keyList[i]]
                } else {
                    let [tmpId, tmpIdIndex] = keyList[i].split("[")
                    tmpIdIndex = tmpIdIndex.replace("]", "")
                    tmpMeta = tmpMeta[tmpId][tmpIdIndex] //outbounds,undefinedのエラーが起きる場合、削除対象の値がありません。
                }
            }
            delete tmpMeta[key.split("[")[key.split("[").length - 1].replace("]", "")]
            setMetadata(tmpMetadata)
        } catch (error) {
            //pass ここに入る場合、削除する値がありません。
        } finally {
            setInputlists(prevItems => prevItems.filter(inputlist => inputlist.key !== key))
        }
    }

    function deleteArray() {
        setCount(0)
        setInputlists([])

    }

    function togglePanel() {
        // toggleの値をclassに入れるので空白を入れています。
        if (toggle === " hidden") {
            setToggle("")
        } else {
            setToggle(" hidden")
        }
    }

    return (
        <fieldset className="schema-form-fieldset flexbox" id={childId} name={form.key.split(".")[form.key.split(".").length - 1]}>
            <div className="panel panel-default deposit-panel">
                <div className="panel-heading" onClick={() => togglePanel()}>
                    <a className="panel-toggle" onClick={() => togglePanel()}>
                        {("title_i18n" in form) && ("ja" in form.title_i18n) ? form.title_i18n.ja : form.title}
                    </a>
                    <div className="pull-right">{isRequired ? "Required" : "Optional"}</div>
                </div>
                <div className={"panel-body panel-body2 list-group" + toggle}>
                    <div className="schema-form-array">
                        <div className="col-sm-12">
                            {(form.type === "contentfile") && <FileUploadForm addArray={addArray} deleteArray={deleteArray} />}
                            {(form.type === "thumbnail") && <ThumbnailUploadForm addArray={addArray} deleteArray={deleteArray} />}
                            {inputlists.map((inputlist, index) => (
                                <li className="list-group-item ui-sortable" id={childId + "[" + index + "]"} key={inputlist.key}>
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
                            (<button onClick={() => addArray()} type="button" className={"btn btn-success pull-right"}>
                                <i className="glyphicon glyphicon-plus"></i>
                                New
                            </button>)}
                    </div>
                </div>
            </div>
        </fieldset >
    )
}

function Inputlist({ form, count, childId }) {
    const inputField = [];
    let childIdWithIndex = childId + "[" + count + "]"
    if (!("items" in form)) {
        inputField.push(<Datepickerform order={count} item={form} key={form.key} />);
    } else {
        form.items.forEach(item => {
            if ("type" in item) {
                if (item.type === "text") {
                    inputField.push(
                        <Textform value={""} parentId={childIdWithIndex} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "textarea") {
                    inputField.push(
                        <Textareaform parentId={childIdWithIndex} value={""} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "select") {
                    inputField.push(
                        <Selectform map={item.titleMap} parentId={childIdWithIndex} value={""} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "radios") {
                    inputField.push(
                        <Radioform map={item.titleMap} parentId={childIdWithIndex} value={""} order={count} item={item} key={item.key} />
                    );
                } else if (item.type === "fieldset") {
                    inputField.push(<Panelform form={item} parentId={childIdWithIndex} key={item.key} />);
                } else if (item.type === "contentfile" || item.type === "thumbnail") {
                    inputField.push(<Panelform form={item} parentId={childIdWithIndex} key={item.key} />);
                } else if (item.type === "template") {
                    if ("templateUrl" in item) {
                        let template = item.templateUrl.split('/').pop()
                        if (template === "datepicker.html" || template === "datepicker_multi_format.html") {
                            inputField.push(<Datepickerform order={count} parentId={childIdWithIndex} item={item} key={item.key} />);
                        } else if (template === "datalist.html") {
                            inputField.push(<FileNameform order={count} parentId={childIdWithIndex} item={item} key={item.key} />);
                        } else if (template === "checkboxes.html") {
                            inputField.push(<Checkboxesform order={count} parentId={childIdWithIndex} item={item} map={item.titleMap} key={item.key} />)
                        }
                    } else if ("template" in item) {
                        inputField.push(<div></div>);
                    }
                } else {
                    inputField.push(<div></div>);
                }

            } else {
                inputField.push(<Panelform form={item} parentId={childIdWithIndex} key={item.key} />);
            }
        })
    };
    return (
        <div className="list-group">
            {inputField}
        </div>
    );
}

function Metadatatitle({ item }) {
    let required = false;
    let title = ("title_i18n" in item) && ("ja" in item.title_i18n) ? item.title_i18n.ja : item.title
    let classValue;
    if (schema.required.includes(item.key.split(".")[0].replace("[]", ""))) {
        required = true;
    }
    if (required) {
        classValue = "col-sm-3 control-label field-required";
    } else {
        classValue = "col-sm-3 control-label";
    }
    return (
        <label className={classValue}>
            {title}
        </label>
    )
}

function Textform({ item, parentId }) {
    const metadata = useMetadataValue();
    const changeMetadata = useMetadataChangeValue();
    const formId = parentId + "." + item.key.split(".")[item.key.split(".").length - 1]
    let readOnly = false;

    if ("readonly" in item && item.readonly === true) {
        readOnly = true;
    }
    return (
        <div className="form-group schema-form-text">
            <Metadatatitle item={item} />
            <div className="col-sm-9">
                <input type="text"
                    className="form-control input-form"
                    id={formId}
                    name={item.key.split(".")[item.key.split(".").length - 1]}
                    schema-validate="form"
                    disabled={readOnly}
                    defaultValue={getMetadata(formId, metadata)}
                    onBlur={(e) => changeMetadata(formId, e.target.value)}
                ></input>
            </div>
        </div>
    );
}


function Selectform({ parentId, map, item }) {
    const metadata = useMetadataValue();
    const editMetadata = useMetadataEditValue();
    const setMetadata = useMetadataSetValue();
    const titleMap = [];
    const formId = parentId + "." + item.key.split(".")[item.key.split(".").length - 1]
    function selectOnChange(formId, value) {
        // change select value
        let tmpMetadata = structuredClone(metadata)
        editMetadata(tmpMetadata, formId, value)
        // use onChange
        if (item.hasOwnProperty("onChange")) {
            const onChange = item.onChange
            editMetadata(tmpMetadata, parentId + "." + onChange.changekey, onChange.keyvalue[value])
        }
        setMetadata(tmpMetadata)
    }
    map.forEach(element => {
        titleMap.push(
            <option label={element.name} value={element.value} key={formId + element.value}></option>
        );
    })
    return (
        <div className="form-group schema-form-select">
            <Metadatatitle item={item} />
            <div className="col-sm-9">
                <select className="form-control input-form"
                    schema-validate="form"
                    id={formId}
                    name={item.key.split(".")[item.key.split(".").length - 1]}
                    value={getMetadata(formId, metadata) || ""}
                    onChange={(e) => selectOnChange(formId, e.target.value)}>
                    <option value=""></option>
                    {titleMap}
                </select>
            </div>
        </div>

    )
}


function Datepickerform({ parentId, item }) {
    const changeMetadata = useMetadataChangeValue();
    const metadata = useMetadataValue();
    const formId = parentId + "." + item.key.split(".")[item.key.split(".").length - 1]
    return (
        <div className="form-group schema-form-datepicker">
            <Metadatatitle item={item} />

            <div className="col-sm-9">
                <input type="date"
                    className="form-control input-form"
                    id={formId}
                    name={item.key.split(".")[item.key.split(".").length - 1]}
                    schema-validate="form"
                    defaultValue={getMetadata(formId, metadata)}
                    onBlur={(e) => changeMetadata(formId, e.target.value)}
                ></input>
            </div>
        </div>
    )
}

function Textareaform({ parentId, item }) {
    const changeMetadata = useMetadataChangeValue();
    const metadata = useMetadataValue();
    const formId = parentId + "." + item.key.split(".")[item.key.split(".").length - 1]
    return (
        <div className="form-group schema-form-textarea">
            <Metadatatitle item={item} />
            <div className="col-sm-9">
                <textarea className="form-control input-form"
                    id={formId}
                    name={item.key.split(".")[item.key.split(".").length - 1]}
                    schema-validate="form"
                    defaultValue={getMetadata(formId, metadata)}
                    onBlur={(e) => changeMetadata(formId, e.target.value)}
                ></textarea>
            </div>
        </div>
    );
}



// 未完成jpcoar2.0では使わない
function Radioform({ parentId, map, order, value, item }) {
    const titleMap = [];
    map.forEach(element => {
        titleMap.push(
            <div className="radio">
                <label>
                    <input type="radio"
                        id={parentId + "." + item.key.split(".")[item.key.split(".").length - 1]}
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
                {titleMap}
            </div>
        </div>
    )
}




// 未完成jpcoar2.0では使わない
function Checkboxesform({ parentId, order, value, item }) {
    const titleMap = [];
    map = item.titleMap
    map.forEach(element => {
        titleMap.push(
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
                    <select sf-changed="form" className="form-control" schema-validate="form" id={parentId + "." + item.key.split(".")[item.key.split(".").length - 1]} defaultValue={value}>
                        <option className value=""></option>
                        {titleMap}
                    </select>
                </div>
            </div>
        </div>
    )
}

/**
 * このメソッドは引数metadataから引数keyの値を取り出すことを目的にしています。
 * @param {string} key 
 * @param {dict} metadata 
 * @returns 
 */
function getMetadata(key, metadata) {
    let keyList = key.split(".")
    let tmpMeta = metadata
    try {
        for (let i = 0; i < keyList.length; i++) {
            // リスト最後の場合
            if (i === keyList.length - 1) {
                return tmpMeta[keyList[i]]
            } else {
                let [tmpId, tmpIdIndex] = keyList[i].split("[")
                tmpIdIndex = tmpIdIndex.replace("]", "")
                tmpMeta = tmpMeta[tmpId][tmpIdIndex]
            }
        }
    } catch (error) {
        return undefined
    }
    return tmpMeta
}

/**
 * 引数のHTMLごとに辞書を作成していくことを目的にしているメソッドです。
 * @param {HTMLElement} panel 
 * @param {dict} property 
 * @param {int} nest 
 */
function readPanel(panel, property, nest) {
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
                        readPanel(elem, proper, nest + 1)
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

/**
 * このメソッドは画面に入力された情報を取り出し、想定されている形の辞書型に成形することを目的にしています。
 * @returns {dict} 
 */
function readMetadata() {
    let itemMetadata = {}
    // 項目ごとにHTMLを取得
    document.querySelectorAll('.form_metadata_property').forEach(function (element) {

        //項目の大枠を取得
        let metadataProperty = element.querySelector('.schema-form-fieldset');

        // itemMetadataに項目のキーを追加し、操作できるようにする。
        itemMetadata[metadataProperty.name] = []

        let properties = itemMetadata[metadataProperty.name]

        metadataProperty.querySelectorAll('li.list-group-item.ui-sortable').forEach(function (elemen) {
            if (elemen.id.split(".").length === 1) {
                let property = {}
                elemen.querySelectorAll('.input-form.form-control').forEach(function (e) {
                    if (e.id.split('.').length <= 2) {
                        if (e.value != "") {
                            property[e.name] = e.value;
                        }
                    }
                })

                readPanel(elemen, property, 2)
                if (Object.keys(property).length) {
                    properties.push(property)
                }
            }
        })
        // 入力がない項目のキーを削除
        if (!(properties.length)) {
            delete itemMetadata[metadataProperty.name];
        }
    })

    return itemMetadata
}

/**
 * このメソッドは引数required_listに入っている項目の値が入力されているかどうかを確認することを目的にしています。
 * 入力されていなかった場合、その項目の入力欄を赤くハイライトさせます。
 * また、その項目を返り値のarrayにいれます。
 * @param {Array} required_list 
 * @returns {Array}
 */
function checkRequired(required_list) {
    let requiredButNoValueList = new Set();
    required_list.forEach(function (element) {
        const required_panel = document.getElementById(element);
        required_panel.querySelectorAll('.input-form.form-control').forEach(function (ele) {
            if (ele.value === undefined || ele.value === "") {
                ele.style.border = '1px solid #a94442';// 赤
                requiredButNoValueList.add(element);
            } else {
                ele.style.border = '';
            }
        })
    })
    return Array.from(requiredButNoValueList);
}

/**
 * このメソッドは引数Fileオブジェクトが100MBを超えているかどうかを確認することを目的にしています。
 * 超えていた場合Trueを超えていない場合Falseを返します。
 * @param {File} file 
 * @returns 
 */
function checkFilesizeOver100MB(file) {
    /// ファイルサイズ取得
    const fileSize = file.size;
    /// MB単位のファイルサイズ計算
    const fileMib = fileSize / 1024 ** 2;
    return !(fileMib < 100)
}

const root = createRoot(document.getElementById('input_form_container'));
Modal.setAppElement(document.getElementById('input_form_container'));
let forms = null;
let schema = null;
const urls = ['/static/json/form.json', '/static/json/jsonschema.json']

const promises = urls.map(url =>
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(NETWORK_ERROR_MESSAGE);
            }
            return response.json();
        })
        .catch(error => {
            console.error(FETCH_ERROR_MESSAGE + ':', error);
            alert(FETCH_ERROR_MESSAGE)
        })
);

Promise.all(promises)
    .then(response => {
        forms = response[0]
        schema = response[1]
        root.render(<ItemRegisterTabPage />);
    })
    .catch(error => {
        console.error(FETCH_ERROR_MESSAGE + ':', error);
        alert(FETCH_ERROR_MESSAGE)
    });


