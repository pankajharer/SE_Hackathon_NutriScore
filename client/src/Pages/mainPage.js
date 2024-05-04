import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './mainPage.css';

function MainPage() {
    const [productInfo, setProductInfo] = useState(null);
    const [isScanning, setIsScanning] = useState(false);
    const [showPleaseWaitPopup, setShowPleaseWaitPopup] = useState(false);
    const [showPlaceQRPopup, setShowPlaceQRPopup] = useState(false);
    const [showWrongQRPopup, setShowWrongQRPopup] = useState(false);

    

    const handleScanButtonClick = async () => {
        try {
            let timeout;
            // Show "Please wait" popup immediately
            setShowPleaseWaitPopup(true);
            timeout = setTimeout(() => {
              setShowPleaseWaitPopup(false);
              setShowPlaceQRPopup(true);
          }, 8000);
            // Set scanning state to true
            setIsScanning(true);

            // Make a GET request to initiate barcode scanning
            const response = await axios.get('http://127.0.0.1:5000/scan');
            const productData = response.data.productInfo;
            console.log('Product Data:', productData);

            // Update productInfo state with the retrieved product data
            setProductInfo(productData);
            setShowPlaceQRPopup(false);
            if (!productData) {
              setShowPlaceQRPopup(false);
              setShowWrongQRPopup(true);
          }
        } catch (error) {
            console.error('Error scanning barcode:', error);
        } finally {
            // Update scanning state back to false when the operation is complete
            setIsScanning(false);
        }
    };

    const closeWrongQRPopup = () => {
        setShowWrongQRPopup(false);
    };

    return (
        <div className="container">
            <header className="header">
                <h1>Product Evaluation</h1>
                <button className="scan-btn" onClick={handleScanButtonClick}>
                    Scan
                </button>
            </header>
            <div className="camera-container">
                {showPleaseWaitPopup && (
                    <div className="overlay-loader">
                        <div className="popup-loader">
                            <p>Please wait...</p>
                        </div>
                    </div>
                )}

                {showPlaceQRPopup && (
                    <div className="overlay">
                        <div className="popup">
                            <p style={{ fontWeight: 'bolder' }}>Place your barcode in front of the camera...</p>
                        </div>
                    </div>
                )}

                {showWrongQRPopup && (
                    <div className="overlay">
                        <div className="popup">
                            <p>Wrong QR code. Please try again.</p>
                            <button onClick={closeWrongQRPopup}>Close</button>
                        </div>
                    </div>
                )}
            </div>
            <div className="table-container">
                <h2>Results</h2>
                <table className="results-table">
                    <thead>
                        <tr>
                            <th>Product ID</th>
                            <th>Name</th>
                            <th>Brand</th>
                            <th>Category</th>
                            <th>Ingredients</th>
                            <th>Allergens</th>
                            <th>Additives</th>
                            <th>Price (Rs)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {productInfo && (
                            <tr>
                                <td>{productInfo.product_id}</td>
                                <td>{productInfo.name}</td>
                                <td>{productInfo.brand}</td>
                                <td>{productInfo.category}</td>
                                <td>{productInfo.ingredients.join(', ')}</td>
                                <td>{productInfo.allergens.join(', ')}</td>
                                <td>{productInfo.additives.join(', ')}</td>
                                <td>{productInfo.price}</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            <div className="info-section">
            <h2>Further Information</h2>
            {productInfo && (
                <ul>
                    <li>Calories: {productInfo.nutritional_information.calories}</li>
                    <li>Fat: {productInfo.nutritional_information.negative.fat}g</li>
                    <li>Saturated Fat: {productInfo.nutritional_information.negative.saturated_fat}g</li>
                    <li>Trans Fat: {productInfo.nutritional_information.negative.trans_fat}g</li>
                    <li>Cholesterol: {productInfo.nutritional_information.negative.cholesterol}g</li>
                    <li>Sodium: {productInfo.nutritional_information.negative.sodium}g</li>
                    <li>Carbohydrates: {productInfo.nutritional_information.positive.carbohydrates}g</li>
                    <li>Protein: {productInfo.nutritional_information.positive.protein}g</li>
                    <li>Fiber: {productInfo.nutritional_information.positive.fiber}g</li>
                    <li>Sugars: {productInfo.nutritional_information.positive.sugars}g</li>
                    <li>Vitamin A: {productInfo.nutritional_information.positive.vitamin_a}%</li>
                    <li>Vitamin C: {productInfo.nutritional_information.positive.vitamin_c}%</li>
                    <li>Calcium: {productInfo.nutritional_information.positive.calcium}%</li>
                    <li>Iron: {productInfo.nutritional_information.positive.iron}%</li>
                </ul>
            )}
            <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed auctor,
                magna id commodo bibendum, dui velit bibendum lorem, non ullamcorper
                turpis ex ac risus. Nullam vel lacus eu mauris ultrices facilisis.
            </p>
            {productInfo && (
                <div className='Product_image'>
                    <img src={productInfo.image} alt="No Image"/>
                </div>
            )}
        </div>

        

        </div>
    );
}

export default MainPage;
